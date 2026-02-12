from yt_dlp import YoutubeDL
import json
import re

def searchVideo(query):
    ydl_opts = {
        "quiet" : True,
        "skip_download": True,
        "extract_flat": False,  
        "dump_single_json": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        return info["entries"][0]  
    
def topTimetamp(video, ignore_secs=30):
    heatmap = video.get("heatmap")
    if not heatmap:
        return None

    filtered = [
        s for s in heatmap
        if s["start_time"] > ignore_secs
    ]
    best = max(filtered, key=lambda x: x["value"])
    return best["start_time"]

def downloadVideo(video, start, end):

    fixed_title = video['title'].replace(" ", "_")
    fixed_title = re.sub(r"[^a-zA-Z0-9_]", "", fixed_title)

    ffmpeg_args = {
        "ffmpeg_i" : ["-ss", str(start), "-to", str(end)],
    }

    ydl_opts = {
        "format": "bestaudio",
        "external_downloader": "ffmpeg",
        "external_downloader_args": ffmpeg_args,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": f"music/{fixed_title}.%(ext)s"
    }

    with YoutubeDL(ydl_opts) as ytdl:
        ytdl.download(video["webpage_url"])


def getClip(song_name):
    print(song_name)
    video = searchVideo(song_name)
    print(video["title"])
    print(video["webpage_url"])
    drop = topTimetamp(video)
    if drop:
        print('drop at', drop)
        downloadVideo(video, drop, (drop + 5))
    else:
        print(song_name, "couldnt get drop")


songs_json = open("songs.json").read()
names = json.loads(songs_json)

from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(getClip, name) for name in names]

    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print("Error:", e)

