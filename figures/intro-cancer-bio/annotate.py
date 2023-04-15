#!/usr/bin/env python

import argparse
from PIL import Image

def get_text_dimensions(text, font):
    ascent, descent = font.getmetrics()

    width = font.getmask(text).getbbox()[2]
    height = font.getmask(text).getbbox()[3] + descent

    return width, height


def main(fname):
    img = Image.open(fname)
    w, h = img.size

    extended = Image.new("RGB", (w, h + ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    main(args.filename)