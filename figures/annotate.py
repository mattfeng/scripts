#!/usr/bin/env python

import argparse
from PIL import Image, ImageDraw, ImageFont
from os.path import splitext, basename

shortcuts = {
    "weinberg": "Weinberg, The Biology of Cancer [2e]"
}

def get_text_height(text, font, margin=10):
    ascent, descent = font.getmetrics()

    heights = [
        font.getmask(line).getbbox()[3] + descent + margin
        for line in text
    ]
    heights[-1] -= margin

    return heights

def wrap(text, font, max_pixels):
    build = []
    lines = []
    for word in text.split(" "):
        test = " ".join(build + [word])

        width = font.getmask(test).getbbox()[2]

        if width > max_pixels:
            lines.append(" ".join(build))
            build = [word]
        else:
            build.append(word)
    
    lines.append(" ".join(build))

    return lines

def main(fname):
    img = Image.open(fname)
    title, _ = splitext(basename(fname))
    w, h = img.size

    source = input("Source: ")
    if source in shortcuts:
        source = shortcuts[source]
    label = f"{title} (source: {source})"

    font = ImageFont.truetype("arial.ttf", int(w ** 0.5))

    label = wrap(label, font, w)

    label_heights = get_text_height(label, font)

    extended = Image.new("RGB", (w, h + sum(label_heights)), color="white")
    extended.paste(img)

    draw = ImageDraw.Draw(extended)

    y = h
    for i, line in enumerate(label):
        draw.text((10, y), line, font=font, fill="black")
        y += label_heights[i]

    extended.save(f"{title} (out).png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    main(args.filename)