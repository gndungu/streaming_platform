import os
import subprocess

def convert_to_hls(video_instance):

    input_path = video_instance.file.path

    output_dir = os.path.splitext(input_path)[0]

    os.makedirs(output_dir, exist_ok=True)

    playlist_path = os.path.join(output_dir, "master.m3u8")

    command = [
        "ffmpeg",
        "-i", input_path,

        # VIDEO
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",

        # AUDIO
        "-c:a", "aac",
        "-b:a", "128k",

        # HLS
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-f", "hls",

        playlist_path
    ]

    subprocess.run(command, check=True)

    with open(playlist_path, "rb") as f:
        video_instance.master_playlist_url.save(
            os.path.basename(playlist_path),
            File(f),
            save=True
        )

    return playlist_path


def convert_video(video_instance):

    input_path = video_instance.file.path

    output_path = os.path.splitext(input_path)[0] + ".mp4"

    command = [
        "ffmpeg",
        "-y",                    # overwrite output
        "-i", input_path,

        # VIDEO
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",

        # AUDIO
        "-c:a", "aac",
        "-b:a", "128k",

        # STREAMING OPTIMIZATION
        "-movflags", "+faststart",

        # OUTPUT
        output_path
    ]

    subprocess.run(command, check=True)

    with open(output_path, "rb") as f:
        video_instance.file.save(
            os.path.basename(output_path),
            File(f),
            save=True
        )