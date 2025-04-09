import os
import cv2
import numpy as np
import subprocess
from pathlib import Path
from gpmf import GPMFParser
import scipy.interpolate

INPUT_EXTS = [".mp4", ".lrv"]
OUTPUT_DIR_NAME = "stable"


def extract_gyro(input_path):
    with open(input_path, "rb") as f:
        parser = GPMFParser(f.read())

    telemetry = parser.extract_device_data()

    gyro_tracks = [track for track in telemetry if track["FourCC"] == "GYRO"]
    if not gyro_tracks:
        raise ValueError("No GYRO track found in telemetry")

    gyro_track = gyro_tracks[0]
    samples = gyro_track["samples"]
    sample_rate = gyro_track["sample_rate"]
    if not sample_rate:
        raise ValueError("No sample rate available for gyro track")

    gyro_data = []
    for i, sample in enumerate(samples):
        timestamp = i / sample_rate
        x, y, z = sample
        gyro_data.append({"timestamp": timestamp, "x": x, "y": y, "z": z})
    return gyro_data


def integrate_gyro(data, axis):
    angles = [0]
    for i in range(1, len(data)):
        dt = data[i]["timestamp"] - data[i - 1]["timestamp"]
        omega = data[i][axis]
        angles.append(angles[-1] + omega * dt)
    return np.array(angles)


def smooth_angles(angles, window=30):
    return np.convolve(angles, np.ones(window) / window, mode="same")


def get_rotation_matrix(gyro_data, timestamps, frame_shape, smoothing_window=30):
    ts = np.array([g["timestamp"] for g in gyro_data])
    pitch = integrate_gyro(gyro_data, "x")
    yaw = integrate_gyro(gyro_data, "y")
    roll = integrate_gyro(gyro_data, "z")

    pitch = smooth_angles(pitch, smoothing_window)
    yaw = smooth_angles(yaw, smoothing_window)
    roll = smooth_angles(roll, smoothing_window)

    interp_roll = scipy.interpolate.interp1d(
        ts, roll, bounds_error=False, fill_value="extrapolate"
    )

    h, w = frame_shape[:2]
    center = (w // 2, h // 2)
    transforms = []

    for t in timestamps:
        angle = -interp_roll(t) * 180 / np.pi  # radians to degrees
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        transforms.append(M)

    return transforms


def stabilize_video(input_path, output_path, gyro_data):
    cap = cv2.VideoCapture(str(input_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    timestamps = np.linspace(0, frames / fps, frames)

    ret, first_frame = cap.read()
    if not ret:
        raise RuntimeError("Could not read video")

    transforms = get_rotation_matrix(gyro_data, timestamps, first_frame.shape)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    temp_path = input_path.with_suffix(".temp.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(temp_path), fourcc, fps, (width, height))

    use_cuda = cv2.cuda.getCudaEnabledDeviceCount() > 0
    crop_margin = 30
    idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or idx >= len(transforms):
            break

        M = transforms[idx]

        if use_cuda:
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)
            gpu_warp = cv2.cuda.warpAffine(gpu_frame, M, (width, height))
            stabilized = gpu_warp.download()
        else:
            stabilized = cv2.warpAffine(frame, M, (width, height))

        cropped = stabilized[crop_margin:height - crop_margin, crop_margin:width - crop_margin]
        resized = cv2.resize(cropped, (width, height))
        out.write(resized)
        idx += 1

    cap.release()
    out.release()

    subprocess.run([
        "ffmpeg", "-y", "-i", str(temp_path),
        "-vcodec", "libx264", "-crf", "23",
        str(output_path)
    ])
    temp_path.unlink()


def main(folder_path):
    folder = Path(folder_path)
    stable_dir = folder / OUTPUT_DIR_NAME
    stable_dir.mkdir(exist_ok=True)

    for file in folder.iterdir():
        if file.suffix.lower() not in INPUT_EXTS:
            continue
        output_file = stable_dir / file.name
        if output_file.exists():
            print(f"Skipping {file.name} (already stabilized)")
            continue

        print(f"Stabilizing {file.name}")
        try:
            gyro = extract_gyro(file)
            stabilize_video(file, output_file, gyro)
        except Exception as e:
            print(f"Failed to stabilize {file.name}: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python gopro_stabilize.py /path/to/folder")
    else:
        main(sys.argv[1])
