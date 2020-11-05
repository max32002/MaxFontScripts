#!/usr/bin/env python3
#encoding=utf-8

import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def draw_single_char(ch, font, canvas_size, x_offset, y_offset):
    img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
    return img

src = '/Users/chunyuyao/Documents/git/SweiSansCJKtc-Regular.otf'
char_size = 1000
canvas_size = 1000
x_offset = 0
y_offset = -280
src_font = ImageFont.truetype(src, size=char_size)

ch='㙊'
ch='體'
ch='源'
ch='姚'

sample_dir = "."
img = draw_single_char(ch, src_font, canvas_size, x_offset, y_offset)
img.save(os.path.join(sample_dir, "U_%d.jpg" % (ord(ch))))