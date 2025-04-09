#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess

import cv2
import cv2
import cv2
import cv2
import numpy as np

from models import get_all_projects
from process_segments import extract_segment


def get_rotation_metadata(filepath):
    """Try to extract rotation angle from both tags and side_data_list via ffprobe."""
    try:
        # First try: look in tags
        cmd_tags = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream_tags=rotate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filepath
        ]
        output = subprocess.check_output(cmd_tags, stderr=subprocess.DEVNULL).decode().strip()
        if output:
            return int(output)

        # Second try: look in side_data_list
        cmd_side_data = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=side_data_list",
            "-of", "json",
            filepath
        ]
        output = subprocess.check_output(cmd_side_data, stderr=subprocess.DEVNULL).decode()
        side_data = json.loads(output)
        items = side_data.get("streams", [])[0].get("side_data_list", [])
        for item in items:
            if item.get("rotation") is not None:
                return int(item["rotation"])
    except Exception as e:
        print(f"⚠️ ffprobe failed to read rotation: {e}")

    return 0  # Default: no rotation

def stabilize(video, segment, segment_filepath: str, alpha=0):
    start_time = segment.start_time
    end_time = segment.end_time

    # Load gyro and accel data
    gyro_filepath = os.path.join("./projects", video.project_dir_name, video.mp4_filename.replace(".MP4", ".gyro.json"))
    accel_filepath = os.path.join("./projects", video.project_dir_name, video.mp4_filename.replace(".MP4", ".accel.json"))
    mp4_filepath = os.path.join("./projects", video.project_dir_name, video.mp4_filename)

    with open(gyro_filepath) as f:
        gyro_data = json.load(f)
    with open(accel_filepath) as f:
        accel_data = json.load(f)

    # Filter to segment time
    gyro_data = [d for d in gyro_data if start_time <= d["timestamp"] <= end_time]
    accel_data = [d for d in accel_data if start_time <= d["timestamp"] <= end_time]

    if not gyro_data or not accel_data:
        raise ValueError("No telemetry data found in segment time range.")

    # Sync lengths
    min_len = min(len(gyro_data), len(accel_data))
    gyro_data = gyro_data[:min_len]
    accel_data = accel_data[:min_len]

    # Extract values
    timestamps = np.array([d["timestamp"] - start_time for d in gyro_data])  # relative
    gyro_x = np.array([d["x"] for d in gyro_data])  # deg/sec
    accel_y = np.array([d["y"] for d in accel_data])
    accel_z = np.array([d["z"] for d in accel_data])
    dt = np.gradient(timestamps)

    accel_roll = np.degrees(np.arctan2(accel_y, accel_z))

    # Complementary filter
    roll = np.zeros_like(accel_roll)
    roll[0] = accel_roll[0]
    for i in range(1, len(roll)):
        delta_gyro = gyro_x[i] * dt[i]
        roll[i] = alpha * (roll[i - 1] + delta_gyro) + (1 - alpha) * accel_roll[i]

    # Open video
    cap = cv2.VideoCapture(segment_filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_timestamps = np.arange(frame_count) / fps
    interpolated_roll = np.interp(video_timestamps, timestamps, roll)
    sampled = interpolated_roll[::int(fps / 1)]  # downsample to 1 fps
    fixed_roll_angle = - float(np.median(sampled)) + 90

    # Write stabilized video
    base, ext = os.path.splitext(segment_filepath)
    output_path = f"{base}_stabilized{ext}"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        # if not ret or frame_id >= len(smoothed_roll):
        #     break

        # Apply fixed stabilization angle only — no in-frame rotation for camera orientation
        M = cv2.getRotationMatrix2D((w / 2, h / 2), fixed_roll_angle, 1.0)
        stabilized = cv2.warpAffine(frame, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        out.write(stabilized)
        frame_id += 1

    cap.release()
    out.release()
    print(f"✅ Stabilized video saved to: {output_path}")
    return output_path


def main():
    filepath = "./projects/Garibaldi Neve Traverse/segments/GX010213_segment_27_46.mp4"
    mp4_video = "GX010213.MP4"

    projects = get_all_projects()
    for project in projects:
        for video in project.videos:
            if video.mp4_filename != mp4_video:
                continue
            video.calculate_telemetry()
            video.calculate_suggested_segments()
            for segment in video.segments:
                segment_filepath = extract_segment(video, segment)
                stabilized_filepath = stabilize(video, segment, segment_filepath)
                print(f"Stabilized video saved to: {stabilized_filepath}")
                return



if __name__ == "__main__":
    main()