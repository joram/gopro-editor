import os
import cv2
import numpy as np
import tempfile
import subprocess
from typing import List
from scipy.signal import savgol_filter

from models import Video, Segment  # Replace with your actual models


def generate_segment_filename(video: Video, segment: Segment) -> str:
    base_name, ext = os.path.splitext(video.mp4_filename)
    return f"{base_name}_segment_{int(segment.start_time)}_{int(segment.end_time)}{ext}"

def compute_roll_angles_from_accel(accel_data, accel_timestamps, video_fps, total_frames):
    roll_angles = np.degrees(np.arctan2(accel_data[:, 1], accel_data[:, 2]))

    video_timestamps = np.arange(total_frames) / video_fps
    interpolated = np.interp(video_timestamps, accel_timestamps, roll_angles)

    window = int(video_fps // 2) | 1  # Ensure odd window size
    smoothed = savgol_filter(interpolated, window_length=window, polyorder=3)

    return smoothed

def stabilize_video(input_path, output_path, roll_angles):
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

def stabilize_video_with_audio(video: Video):
    input_file = video.mp4_filename
    output_file = f"projects/{video.project_dir_name}/{os.path.splitext(input_file)[0]}_stabilized.mp4"

    print("Loading accelerometer data...")
    cap = cv2.VideoCapture(input_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    accel_data = np.array([[a['x'], a['y'], a['z']] for a in video.accel])
    accel_timestamps = np.array([a['timestamp'] for a in video.accel])

    print("Computing roll angles from accel data...")
    roll_angles = compute_roll_angles_from_accel(
        accel_data,
        accel_timestamps,
        video_fps=fps,
        total_frames=frame_count
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_video = os.path.join(tmpdir, 'stabilized.mp4')

        print("Stabilizing video...")
        stabilize_video(input_file, temp_video, roll_angles)

        print("Merging with original audio using ffmpeg...")
        subprocess.run([
            'ffmpeg', '-y',
            '-i', temp_video,
            '-i', input_file,
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-map', '0:v:0',
            '-map', '1:a:0?',
            output_file
        ])

    print("Done! Output saved to:", output_file)

def extract_segment(video: Video, segment: Segment):
    input_path = os.path.join("./projects", video.project_dir_name, video.mp4_filename)
    output_filename = generate_segment_filename(video, segment)
    output_path = os.path.join("./projects", video.project_dir_name, "segments",  output_filename)
    stabilized_output_path = os.path.join("./projects", video.project_dir_name, "segments",  f"stabilized_{output_filename}")

    if os.path.exists(stabilized_output_path):
        print(f"Skipping {output_filename}, already stabilized.")
        return

    if os.path.exists(output_path):
        print(f"Skipping {output_filename}, already exists.")
        return

    duration = segment.end_time - segment.start_time
    command = [
        "ffmpeg",
        "-ss", str(segment.start_time),
        "-i", input_path,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ]

    print(f"Extracting {output_filename}")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Stabilize the extracted segment
    print(f"Stabilizing {output_filename}")
    video.calculate_telemetry()
    accel_data = np.array([[a['x'], a['y'], a['z']] for a in video.accel])
    accel_timestamps = np.array([a['timestamp'] for a in video.accel])
    roll_angles = compute_roll_angles_from_accel(
        accel_data=accel_data,
        accel_timestamps=accel_timestamps,
        video_fps=60,
        total_frames=int(duration * 60)
    )

    stabilize_video(output_path, stabilized_output_path, roll_angles)

def join_segments(videos: List[Video]):
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

def process_videos(videos: List[Video]):
    working_dir = os.path.join("./projects", videos[0].project_dir_name, "segments")
    os.makedirs(working_dir, exist_ok=True)
    for video in videos:
        for segment in video.segments:
            extract_segment(video, segment)
    join_segments(videos)
