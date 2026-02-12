# from moviepy.editor import *
from moviepy import *
from moviepy.audio.fx import AudioFadeIn
from moviepy.video.fx import FadeIn, Resize

import random
import os
from datetime import datetime
import json
import sys

os.makedirs("vids", exist_ok=True)

def get_text(w, h, text, font_size):

    words = text.split()
    
    chars_per_line = 1.5 * w / font_size 

    wrapped_text = ""
    line_chars = 0
    num_lines = 1
    for word in words:
        if (line_chars + len(word) + 1) > chars_per_line:
            wrapped_text += "\n"
            line_chars = 0
            num_lines += 1
        
        line_chars += len(word) + 1
        wrapped_text += word 
        wrapped_text += ' '

    # reduce text size if was too big
    interline=int(font_size/5)
    if h < num_lines * (font_size + interline):
        font_size = int(font_size * 0.9)
        font_size, wrapped_text = get_text(w, h, text, font_size)

    return font_size, wrapped_text


def main(quote_index):
 
    quotes_raw = open("quotes.json").read()
    quotes = json.loads(quotes_raw)
    quote_text = quotes[quote_index]

    # pre generate music and backgrounds using automprompt and backgrounds .py, select them randomly for vids
    file_name = random.choice([
        file for file in os.listdir("music")
        if os.path.isfile(os.path.join("music", file))
    ])
    song_path = os.path.join("music", file_name)

    file_name = random.choice([
        file for file in os.listdir("bgs")
        if os.path.isfile(os.path.join("bgs", file))
    ])
    bg_path = os.path.join("bgs", file_name)


    # audio
    music = AudioFileClip(song_path)
    fade_time = music.duration / 2
    music_faded = music.with_effects([afx.AudioFadeIn(fade_time)])

    # background
    bg = ImageClip(bg_path).with_duration(music.duration)
    bg=bg.with_effects([vfx.FadeIn(fade_time,[255, 160, 200])])
    bg = bg.with_effects([vfx.Resize((1080,1920))]) 
    w, h = bg.size

    # format and resize text
    font_size = 200
    font_size, text = get_text(w, h, quote_text, font_size=font_size)
    interline=int(font_size/5)

    date_text = datetime.now()
    date_text = date_text.strftime("%d/%m/%Y")

    date = TextClip(
        text=date_text,
        color="black", 
        font_size = 200,
        size = [w,h]
    ).with_start(0).with_duration(1).with_position('center')
    date = date.with_effects([vfx.CrossFadeOut(1)])

    txt = TextClip(
        text=text, 
        font="Allura.ttf", 
        color="pink", 
        stroke_color="black", 
        stroke_width=3, 
        interline=interline, 
        text_align="center", 
        font_size=font_size,
        method="label",
        size=(w,h)).with_duration(music.duration).with_position('center')

    txt = txt.with_effects([vfx.FadeIn(fade_time,[255, 160, 200])])

    video = CompositeVideoClip([bg, txt, date]).with_audio(music_faded)

    video.write_videofile(f"vids/{quote_index}.mp4", fps=24)

if __name__ == "__main__":
    main(sys.argv[1])