#!/usr/bin/env python3
import os
import ffmpeg as ffmpeg_module
import ffmpeg

from models import Video, Segment, Project, get_all_projects

def create_segment_filename(video: Video, segment: Segment):
    """
    Generate a file for a video segment.

    Parameters:
        video (Video): The video object.
        segment (Segment): The segment object.

    Returns:
        str: The filename for the segment, that has been created
    """
    output_path = segment.filepath(video)
    if os.path.exists(output_path):
        print(f"Skipping {output_path}, already exists.")
        return output_path

    input_path = os.path.join("./projects", video.project_dir_name, video.mp4_filename)
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    ffmpeg.input(input_path).output(output_path, ss=segment.start_time, t=segment.end_time - segment.start_time, vcodec='libx264', acodec='aac', strict='experimental').run(overwrite_output=True)
    print(f"Extracted segment {output_path} from {input_path}")
    return output_path

def fade_video(input_path, output_path, fade_duration=0.25):
    """
    Apply fade in/out effect to a video.

    Parameters:
        input_path (str): Path to the input video.
        output_path (str): Path to save the processed video.
        fade_duration (float): Duration of the fade in/out in seconds.
    """
    # Get video duration
    try:
        probe = ffmpeg.probe(input_path)
        video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        duration = float(video_stream['duration'])
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return

    # Calculate fade out start time
    fade_out_start = duration - fade_duration
    if fade_out_start <= 0:
        print(f"Video too short to apply fade: {input_path}")
        return

    # Apply fade in and fade out
    try:
        (
            ffmpeg
            .input(input_path)
            .video
            .filter('fade', type='in', start_time=0, duration=fade_duration)
            .filter('fade', type='out', start_time=fade_out_start, duration=fade_duration)
            .output(output_path, vcodec='libx264', acodec='aac', strict='experimental')
            .run(overwrite_output=True)
        )
        print(f"Processed {input_path} -> {output_path}")
    except ffmpeg.Error as e:
        print(f"FFmpeg error for {input_path}: {e.stderr.decode()}")

def merge_videos(video_paths, output_path):
    """
    Merge multiple MP4 videos into a single video.

    Parameters:
        video_paths (list of str): List of paths to input MP4 files.
        output_path (str): Path to save the merged video.
    """
    if len(video_paths) == 0:
        raise ValueError("No videos provided for merging.")

    # Create a list of input streams
    inputs = [ffmpeg.input(v) for v in video_paths]

    # Concatenate videos with re-encoding
    try:
        (
            ffmpeg
            .concat(*inputs, v=1, a=1)
            .output(output_path, vcodec='libx264', acodec='aac')
            .run(overwrite_output=True)
        )
        print(f"Merged {len(video_paths)} videos into {output_path}")
    except ffmpeg.Error as e:
        print(f"Error merging videos: {e.stderr.decode()}")

def create_title_card(title, subtitle, output_path, duration=3, resolution=(1280, 720), font_size=48, subtitle_font_size=30):
    """
    Creates a title card video with centered title and subtitle.

    Parameters:
        title (str): Main title text.
        subtitle (str): Subtitle text.
        output_path (str): Where to save the generated title card video.
        duration (int): Duration of the title card in seconds.
        resolution (tuple): Video resolution (width, height).
        font_size (int): Font size for the title.
        subtitle_font_size (int): Font size for the subtitle.
    """
    width, height = resolution
    title_y = "(h/2 - 60)"
    subtitle_y = "(h/2 + 20)"

    (
        ffmpeg
        .input(f'color=c=black:s={width}x{height}:d={duration}', f='lavfi')
        .filter('drawtext',
                text=title,
                font='Arial',
                fontsize=font_size,
                fontcolor='white',
                x='(w-text_w)/2',
                y=title_y)
        .filter('drawtext',
                text=subtitle,
                font='Arial',
                fontsize=subtitle_font_size,
                fontcolor='white',
                x='(w-text_w)/2',
                y=subtitle_y,
                enable='gte(t,0)')
        .output(output_path, vcodec='libx264', pix_fmt='yuv420p')
        .run(overwrite_output=True)
    )
    print(f"Title card created at {output_path}")

def get_video_resolution(filepath):
    """
    Returns the resolution (width, height) of a video.

    Parameters:
        filepath (str): Path to the video file.

    Returns:
        (int, int): Width and height of the video in pixels.
    """
    try:
        probe = ffmpeg.probe(filepath)
        video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height
    except Exception as e:
        print(f"Failed to get resolution for {filepath}: {e}")
        return None, None

def make_final_cut(project: Project):
    completed_fading_segments = []
    total_segments = sum([len(video.segments) for video in project.videos])
    curr_segment = 0
    videos = project.videos
    videos.sort(key=lambda x: x.mp4_filename)
    for video in videos:
        print(f"Processing video {video.mp4_filename}")
        for segment in video.segments:
            create_segment_filename(video, segment)
            input_path = segment.filepath(video)
            output_path = input_path.replace('.mp4', '_faded.mp4')
            curr_segment = curr_segment + 1
            if os.path.exists(output_path):
                print(f"Skipping {output_path}, already exists.")
                completed_fading_segments.append(segment)
                continue
            print(f"Processing segment {curr_segment}/{total_segments}: {input_path}")
            fade_video(input_path, output_path)
            completed_fading_segments.append(output_path)

    title_card_filepath = os.path.join("./projects", project.name, "segments", "title_card.mp4")
    (width, height) = get_video_resolution(os.path.join("./projects",  project.name, project.videos[0].mp4_filename))
    create_title_card("Garibaldi Neve Traverse", "Spring 2025 (John, Nick, Wilson)", title_card_filepath, duration=3, resolution=(width, height), font_size=48, subtitle_font_size=30)

    completed_fading_segments = [title_card_filepath] + completed_fading_segments
    output_path = os.path.join("./projects", project.name, "segments", "final_cut.mp4")
    merge_videos(completed_fading_segments, output_path)

if __name__ == "__main__":
    projects = get_all_projects()
    for project in projects:
        make_final_cut(project)
