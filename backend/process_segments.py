import asyncio
import os
import subprocess
from typing import List

import cv2
import numpy as np
from scipy.signal import savgol_filter

from models import Video, Segment  # Replace with your actual models
from telemetry import get_telemetry


def generate_segment_filename(video: Video, segment: Segment) -> str:
    base_name, ext = os.path.splitext(video.mp4_filename)
    return f"{base_name}_segment_{int(segment.start_time)}_{int(segment.end_time)}{ext}"

def compute_roll_angles_complementary(input_filepath, alpha=0.98):
    telem = get_telemetry(input_filepath)
    accel_data = telem.raw_accel_data
    gyro_data = telem.raw_gyro_data
    timestamps = telem.accel_timestamps
    print(f"Accel: {len(accel_data)}, Gyro: {len(gyro_data)}, timestamps: {len(timestamps)}")

    if len(accel_data) < 2:
        raise ValueError(f"Not enough data for roll calculation. filepath:{input_filepath} Accel: {len(accel_data)}, Gyro: {len(gyro_data)}, timestamps: {len(timestamps)}")

    # Normalize timestamps to seconds
    time_sec = (timestamps - timestamps[0]) / 1000.0
    dt = np.gradient(time_sec)

    # Compute roll from accel
    accel_roll = np.degrees(np.arctan2(accel_data[:, 1], accel_data[:, 2]))

    # Complementary filter to combine
    roll = np.zeros_like(accel_roll)
    roll[0] = accel_roll[0]
    for i in range(1, len(roll)):
        gyro_delta = gyro_data[i] * dt[i]  # assuming degrees/sec
        roll[i] = alpha * (roll[i - 1] + gyro_delta) + (1 - alpha) * accel_roll[i]

    # Interpolate to match video frame timestamps
    video_fps = 60
    video_timestamps = np.arange(0, time_sec[-1], 1 / video_fps)
    interpolated = np.interp(video_timestamps, time_sec, roll)

    # Smooth
    raw_window = int(video_fps // 2) | 1
    max_allowed = len(interpolated)
    window = min(raw_window, max_allowed if max_allowed % 2 == 1 else max_allowed - 1)

    if window >= 5:
        smoothed = savgol_filter(interpolated, window_length=window, polyorder=3)
    else:
        smoothed = interpolated

    return smoothed


def stabilize_video(input_path):
    output_path = input_path.lower().replace(".mp4", "_stabilized.mp4")

    roll_angles = compute_roll_angles_complementary(input_path)
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(3)), int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_id >= len(roll_angles):
            break

        roll = roll_angles[frame_id]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), -roll, 1.0)
        stabilized = cv2.warpAffine(frame, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

        out.write(stabilized)
        frame_id += 1

    cap.release()
    out.release()

    return output_path


def extract_segment(video: Video, segment: Segment):
    input_path = os.path.join("./projects", video.project_dir_name, video.mp4_filename)
    output_filename = generate_segment_filename(video, segment)
    output_path = os.path.join("./projects", video.project_dir_name, "segments",  output_filename)

    if os.path.exists(output_path):
        print(f"Skipping {output_filename}, already exists.")
        return output_path

    duration = segment.end_time - segment.start_time
    command = [
        "ffmpeg",
        "-ss", str(segment.start_time),
        "-i", input_path,
        "-t", str(duration),
        "-map", "0:0",  # video
        "-c", "copy",
        output_path
    ]
    print(f"Extracting segment {output_filename} from {input_path}: {' '.join(command)}")
    subprocess.run(command)

    return output_path


def join_segments(videos: List[Video], msg_queue: asyncio.Queue):
    for video in videos:
        segments = [generate_segment_filename(video, segment) for segment in video.segments]
        output_filename = f"{video.mp4_filename}_joined.mp4"
        output_path = os.path.join("./projects", video.project_dir_name, "segments",  output_filename)

        if os.path.exists(output_path):
            print(f"Skipping {output_filename}, already exists.")
            continue

        with open("segments.txt", "w") as f:
            for segment in segments:
                f.write(f"file '{os.path.join("./projects", video.project_dir_name, "segments", segment)}'\n")

        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", "segments.txt",
            "-c", "copy",
            output_path
        ]

        print(f"Joining segments into {output_filename}")
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def process_videos(videos: List[Video], msg_queue: asyncio.Queue):
    working_dir = os.path.join("./projects", videos[0].project_dir_name, "segments")
    os.makedirs(working_dir, exist_ok=True)
    total_segments = sum(len(video.segments) for video in videos)
    curr_segment = 0

    for video in videos:
        print(f"Processing video {video.mp4_filename}")
        video.calculate_telemetry()
        video.calculate_suggested_segments()
        for segment in video.segments:
            curr_segment += 1
            print(f"Processing segment {curr_segment}/{total_segments} for video {video.mp4_filename}")
            segment_filepath = extract_segment(video, segment)
            # stabilized_segment_filepath = stabilize_video(segment_filepath)



    print("All segments extracted and stabilized.")
    join_segments(videos, msg_queue)
