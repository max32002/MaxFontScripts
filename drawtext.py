# -*- coding: utf-8 -*-

import os

from PIL import Image, ImageDraw, ImageFont

#CANVAS_SIZE = 1024
CANVAS_SIZE = 1000
CHAR_SIZE = CANVAS_SIZE

if __name__ == '__main__':
    #text = "桌"
    text = chr(int('f92d',16))
    filename = ("000000" + str(hex(ord(text)))[2:])[-6:]
    filename = "U_" + filename + ".bmp"

    # create an image
    out = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), 255)

    # get a font
    #src_font = "/Users/chaopan/PycharmProjects/zi2zi/data/raw_fonts/造字工房尚黑纤细超长体.ttf"
    #src_font = "/Users/chunyuyao/Documents/maxai/pcgreat/zi2zi/data/max_fonts/jason2.ttf"
    #src_font = "/Users/chunyuyao/Documents/maxai/pcgreat/zi2zi/data/max_fonts/noto.otf"
    src_font = "/Users/chunyuyao/Documents/maxai/pcgreat/zi2zi/data/max_fonts/SweiGothicLegCJKjp-Regular.ttf"

    #print(os.path.isfile(src_font))
    font = ImageFont.truetype(src_font, CHAR_SIZE)

    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    left, top, right, bottom = font.getmask(text).getbbox()
    #print("ascent, descent:", ascent, descent)
    #print("width, baseline, offset_x, offset_y:", width, baseline, offset_x, offset_y)
    #print("left, top, right, bottom:", left, top, right, bottom)

    # get a drawing context
    d = ImageDraw.Draw(out)

    #d.text((left, top), text, font=font, fill=(0))
    #d.text((0, 0), text, font=font, fill=(0))
    #d.text((0, -1 * offset_y), text, font=font, fill=(0))
    total_height = ascent + descent
    new_offset_y = -1 * ((total_height-CHAR_SIZE)/2)
    #new_offset_y = -1 * (276-51)/2
    #new_offset_y = -1 * (100-50)/2
    
    #print("new_offset_y:", new_offset_y)
    d.text((0, new_offset_y), text, font=font, fill=(0))
    
    out.save(filename)