import atexit
import json
import os
from typing import Optional
import ffmpeg
import numpy as np
from pydantic import BaseModel

from telemetry import get_telemetry


def get_filenames(filenames, ext):
    options = [f for f in filenames if f.lower().endswith(ext)]
    return options


class Segment(BaseModel):
    start_time: float
    end_time: float


class InterestLevel(BaseModel):
    timestamp: float
    interest_level: float


_CACHED_METADATA = None
def get_metadata(project_name, filename):
    global _CACHED_METADATA
    if _CACHED_METADATA is None:
        try:
            with open("metadata_cache.json", "r") as f:
                _CACHED_METADATA = json.load(f)
        except FileNotFoundError:
            _CACHED_METADATA = {}

    filepath = os.path.join("./projects/", project_name, filename)
    if filepath in _CACHED_METADATA:
        return _CACHED_METADATA[filepath]

    try:
        probe = ffmpeg.probe(filepath)
        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None
        )
        if video_stream is None:
            raise ValueError("No video stream found in file")

        duration = float(video_stream['duration'])
        size_bytes = os.path.getsize(filepath)
        _CACHED_METADATA[filepath] = (size_bytes, duration)

        with open("metadata_cache.json", "w") as f:
            json.dump(_CACHED_METADATA, f)

        return size_bytes, duration
    except Exception as e:
        print(f"Error getting metadata: {e}")
        return 0, 0




class Video(BaseModel):
    project_dir_name: str
    length: float
    size_bytes: int
    slug: str
    mp4_filename: str
    lrv_filename: Optional[str]
    thumbnail_filename: Optional[str]
    accel_filename: Optional[str]
    gyro_filename: Optional[str]
    segments_filename: Optional[str]
    suggested_segments: Optional[list[Segment]] = None
    interest_levels: Optional[list[InterestLevel]] = None

    accel: list[dict] = []
    gyro: list[dict] = []
    segments: list[Segment] = []

    @classmethod
    def from_mp4(cls, project_dir_name, mp4_filename, filenames):

        lrv_filenames = get_filenames(filenames, ".lrv")
        thumbnail_filenames = get_filenames(filenames, ".thm")
        accel_filenames = get_filenames(filenames, ".accel.json")
        gyro_filenames = get_filenames(filenames, ".gyro.json")
        segments_filenames = get_filenames(filenames, ".segments.json")


        def get_filename_from_uid(uid, filenames):
            for filename in filenames:
                if uid in filename:
                    return filename
            return None

        uid = mp4_filename.replace(".MP4", "").replace("GX", "")
        lrv_filename = get_filename_from_uid(uid, lrv_filenames)
        thumbnail_filename = get_filename_from_uid(uid, thumbnail_filenames)
        accel_filename = get_filename_from_uid(uid, accel_filenames)
        gyro_filename = get_filename_from_uid(uid, gyro_filenames)
        segments_filename = get_filename_from_uid(uid, segments_filenames)

        segments = []
        interest_levels = []
        if segments_filename is not None:
            segments_filepath = os.path.join("./projects/", os.path.join(project_dir_name, segments_filename))

            with open(segments_filepath, "r") as f:
                content = f.read()
                if content:
                    segments_json = json.loads(content)
                    segments = [Segment(**segment) for segment in segments_json["segments"]]
                    interest_levels = [InterestLevel(**segment) for segment in segments_json.get("interest_levels", [])]
        size_bytes, duration = get_metadata(project_dir_name, mp4_filename)

        video = Video(
            project_dir_name=project_dir_name,
            slug=uid,
            mp4_filename=mp4_filename,
            lrv_filename=lrv_filename,
            thumbnail_filename=thumbnail_filename,
            accel_filename=accel_filename,
            gyro_filename=gyro_filename,
            segments_filename=segments_filename,
            segments=segments,
            suggested_segments=segments,
            interest_levels=interest_levels,
            length=duration,
            size_bytes=size_bytes,
        )
        if len(interest_levels) == 0:
            video.calculate_suggested_segments()

        return video
    def calculate_telemetry(self):
        if self.accel_filename is None:
            self.accel_filename = self.mp4_filename.replace(".MP4", ".accel.json")
        if self.gyro_filename is None:
            self.gyro_filename = self.mp4_filename.replace(".MP4", ".gyro.json")
        accel_filepath = os.path.join("./projects/", os.path.join(self.project_dir_name, self.accel_filename))
        gyro_filepath = os.path.join("./projects/", os.path.join(self.project_dir_name, self.gyro_filename))

        self.accel = []
        if os.path.exists(accel_filepath):
            with open(accel_filepath, "r") as f:
                content = f.read()
                if content:
                    self.accel = json.loads(content)

        self.gyro = []
        if os.path.exists(gyro_filepath):
            with open(gyro_filepath, "r") as f:
                content = f.read()
                if content:
                    self.gyro = json.loads(content)

        if len(self.accel) == 0:
            telemetry = get_telemetry(self.project_dir_name, self.mp4_filename)
            self.accel = telemetry.accel
            self.gyro = telemetry.gyro

            with open(accel_filepath, "w") as f:
                f.write(json.dumps(telemetry.accel, indent=4))

            with open(gyro_filepath, "w") as f:
                f.write(json.dumps(telemetry.gyro, indent=4))

    def shrink_interest_levels_resolution(self):
        if type(self.interest_levels[0].timestamp == int):
            print("Already shrunk")
            return

        values = {}
        for datapoint in self.interest_levels:
            timestamp = int(datapoint.timestamp)
            if timestamp not in values:
                values[timestamp] = []
            values[timestamp].append(datapoint.interest_level)

        self.interest_levels = [
            InterestLevel(timestamp=timestamp, interest_level=float(np.mean(values[timestamp])))
            for timestamp in values
        ]

    def calculate_suggested_segments(self):
        if self.segments_filename is None:
            self.segments_filename = self.mp4_filename.replace(".MP4", ".segments.json")
        filepath = os.path.join("./projects/", os.path.join(self.project_dir_name, self.segments_filename))
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
                if content:
                    segments_json = json.loads(content)
                    self.segments = [Segment(**segment) for segment in segments_json["segments"]]
                    self.suggested_segments = self.segments
                    self.interest_levels = [InterestLevel(**segment) for segment in segments_json.get("interest_levels", [])]
                    if len(self.interest_levels) == 0:
                        self.calculate_telemetry()

        if len(self.interest_levels) == 0:

            self.calculate_telemetry()

            interest_levels = {}
            for datapoint in self.accel:
                timestamp = datapoint["timestamp"]
                if timestamp not in interest_levels:
                    interest = datapoint["x"] + datapoint["y"] + datapoint["z"]
                    interest_levels[timestamp] = interest
            for datapoint in self.gyro:
                timestamp = datapoint["timestamp"]
                if timestamp not in interest_levels:
                    interest = datapoint["x"] + datapoint["y"] + datapoint["z"]
                    interest_levels[timestamp] = interest

            def extract_interesting_segments(
                    data: dict,
                    threshold: float,
                    minimum_length: float = 1,
                    buffer: float = 0.5,
                    merge_distance: float = 3
            ):
                """
                Extracts interesting segments from timestamped interest level data.

                Args:
                    data: Dict of {timestamp: interest_level}.
                    threshold: Interest level threshold to consider a point interesting.
                    minimum_length: Minimum length of segment to include.
                    buffer: Time to add before start and after end of each segment.
                    merge_distance: Merge segments if gap between them is less than this.

                Returns:
                    List of dicts with 'start' and 'end' keys.
                """
                if not data:
                    return []

                segments = []
                sorted_times = sorted(data.keys())
                current_start = None

                for t in sorted_times:
                    interest = data[t]

                    if interest >= threshold:
                        if current_start is None:
                            current_start = t
                    else:
                        if current_start is not None:
                            if t - current_start >= minimum_length:
                                segments.append({
                                    "start": current_start - buffer,
                                    "end": t + buffer
                                })
                            current_start = None

                if current_start is not None:
                    end_time = sorted_times[-1]
                    if end_time - current_start >= minimum_length:
                        segments.append({
                            "start": current_start - buffer,
                            "end": end_time + buffer
                        })

                # Merge segments that are close together
                if not segments:
                    return []

                merged_segments = [
                    Segment(start_time=segments[0]["start"], end_time=segments[0]["end"])
                ]

                for seg in segments[1:]:
                    last = merged_segments[-1]
                    if seg["start"] - last.end_time <= merge_distance:
                        last.end_time = max(last.end_time, seg["end"])
                    else:
                        merged_segments.append(Segment(start_time=seg["start"], end_time=seg["end"]))

                return merged_segments

            def smooth_interest(data: dict, window_size: int = 5) -> dict:
                """
                Smooth interest levels using a simple moving average.

                Args:
                    data: Dict of {timestamp: interest_level}.
                    window_size: Number of points in the moving average window.

                Returns:
                    Dict of {timestamp: smoothed_interest_level}.
                """
                if not data:
                    return {}

                sorted_items = sorted(data.items())
                timestamps = [t for t, _ in sorted_items]
                values = [v for _, v in sorted_items]

                smoothed_values = np.convolve(values, np.ones(window_size) / window_size, mode='same')

                return dict(zip(timestamps, smoothed_values))

            interest_levels = smooth_interest(interest_levels, window_size=300)
            segments = extract_interesting_segments(interest_levels, 10)
            self.suggested_segments = segments
            self.interest_levels = [
                InterestLevel(timestamp=timestamp, interest_level=interest)
                for timestamp, interest in interest_levels.items()
            ]
            self.segments = segments

        self.shrink_interest_levels_resolution()

    def write_segments(self):
        if self.segments_filename is None:
            raise ValueError("No segments filename provided")

        segments_filepath = os.path.join("./projects/", self.project_dir_name, self.segments_filename)
        with open(segments_filepath, "w") as f:
            segments_json = {
                "segments": [json.loads(segment.model_dump_json()) for segment in self.segments],
                "interest_levels": [json.loads(interest_level.model_dump_json()) for interest_level in self.interest_levels],
            }
            f.write(json.dumps(segments_json, indent=4))
        print(f"Wrote {len(self.segments)} segments to", segments_filepath)

class Project(BaseModel):
    name: str
    slug: str
    videos: list[Video]




def get_all_projects():
    projects = []
    for project_name in os.listdir("projects"):
        if os.path.isdir(os.path.join("projects", project_name)):
            filenames = os.listdir(os.path.join("projects", project_name))
            mp4_filenames = get_filenames(filenames, ".mp4")
            project = Project(
                name=project_name,
                slug=project_name.replace(" ", "_").lower(),
                videos=[],
            )
            for mp4_filename in mp4_filenames:
                video = Video.from_mp4(project_name, mp4_filename, filenames)
                # if len(video.segments) == 0:
                #     video.calculate_telemetry()
                project.videos.append(video)
            projects.append(project)
    return projects

def get_project(project_slug):
    projects = get_all_projects()
    for project in projects:
        if project.slug == project_slug:
            return project
