from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


def video_trim(
    link, path=None, filename="video", video_length=5, output_filename="output"
):
    yt = YouTube(link)
    stream = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )

    video_path = (
        str(path) + "/" + str(filename) + ".mp4"
        if path != None
        else str(filename) + ".mp4"
    )

    stream.download(path, filename=filename)
    clip = VideoFileClip(video_path)

    start_time = 0
    end_time = (
        clip.duration if clip.duration <= (60 * video_length) else 60 * video_length
    )
    time_length = clip.duration
    count = 0

    while True:
        targetname_file = (
            str(path) + "/" + str(output_filename) + str(count) + ".mp4"
            if path != None
            else str(output_filename) + str(count) + ".mp4"
        )

        try:
            ffmpeg_extract_subclip(
                video_path, start_time, end_time, targetname=targetname_file,
            )
        except:
            break

        start_time = end_time
        end_time = end_time + 60 * 5
        time_length -= 60 * 5
        count += 1

        if time_length <= 0:
            break


if __name__ == "__main__":
    link = input("YouTube link: ")
    video_trim(link)
