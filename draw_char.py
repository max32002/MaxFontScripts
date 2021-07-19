#!/usr/bin/env python3
#encoding=utf-8

import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import argparse

def draw_single_char(ch, font, canvas_size, x_offset, y_offset):
    img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
    return img

def export(src_font_path, char_size, canvas_size, x_offset, y_offset, char, sample_dir, filename_pattern, filename_source):
    #src_font_path = '/Users/chunyuyao/Documents/git/SweiSansCJKtc-Regular.otf'
    #char_size = 1000
    #canvas_size = 1000
    #x_offset = 0
    #y_offset = -280
    src_font = ImageFont.truetype(src_font_path, size=char_size)

    #char='姚'
    #sample_dir = "."

    unicode_int = ord(char)
    filename_variable = char
    if filename_source == 'unicode_hex':
        filename_variable = str(hex(unicode_int))[2:]
    if filename_source == 'unicode_int':
        filename_variable = unicode_int
    filename=filename_pattern % (filename_variable)

    final_filepath = os.path.join(sample_dir,filename)

    img = draw_single_char(char, src_font, canvas_size, x_offset, y_offset)
    img.save(final_filepath)

def cli():
    parser = argparse.ArgumentParser(
            description="draw fonts using FontForge")

    parser.add_argument("--font",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--canvas_size",
        help="canvas size",
        default=1000,
        type=int)

    parser.add_argument("--char_size",
        help="char size",
        default=1000,
        type=int)

    parser.add_argument("--x_offset",
        help="x offset",
        default=0,
        type=int)

    parser.add_argument("--y_offset",
        help="y offset",
        default=0,
        type=int)

    parser.add_argument("--string",
        help="draw chars",
        default=None,
        required=True,
        type=str)

    parser.add_argument("--output",
        help="sample dir",
        default=".",
        type=str)

    parser.add_argument("--filename_pattern",
        help="output filename pattern",
        default="U_%s.bmp",
        type=str)

    parser.add_argument("--filename_source", type=str, choices=['char', 'unicode_hex', 'unicode_int'],
        help='svg filename pattern source.\n'
             'use char for character.\n'
             'use unicode_hex for unicode hex .\n'
             'use unicode_hex for unicode decimal.',
        default="unicode_int",
        )

    args = parser.parse_args()

    is_pass_check = True 
    error_message = ""

    chars = args.string

    if len(chars) < 1:
        is_pass_check = False
        error_message = "Char is required"

    cnt = 0
    if is_pass_check:
        print("Start to draw chars...")
        for char in chars:
            cnt += 1
            export(args.font, args.char_size, args.canvas_size, args.x_offset, args.y_offset, char, args.output, args.filename_pattern, args.filename_source)
    else:
        print("Error: %s" % (error_message))

    if cnt > 0:
        print("Draw char count: %d" % (cnt))

if __name__ == "__main__":
    cli()
