#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import exists

import numpy as np
from PIL import Image
import argparse


def changeColor(im, original_value, target_value):
    data = np.array(im)

    r1, g1, b1 = original_value
    r2, g2, b2 = target_value

    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]
    
    im = Image.fromarray(data)
    return im

def main():
    parser = argparse.ArgumentParser(description='ChangeColor')
    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default=None,
        type=str)

    parser.add_argument("--from_r",
        help="from RED color",
        default=0,
        type=int)
    parser.add_argument("--from_g",
        help="from GREEN color",
        default=0,
        type=int)
    parser.add_argument("--from_b",
        help="from BLUE color",
        default=0,
        type=int)

    parser.add_argument("--to_r",
        help="to RED color",
        default=255,
        type=int)
    parser.add_argument("--to_g",
        help="to GREEN color",
        default=0,
        type=int)
    parser.add_argument("--to_b",
        help="to BLUE color",
        default=0,
        type=int)

    parser.add_argument("--resize_canvas_size",
        help="resize canvas to new size",
        default=None,
        type=int)

    # default is not overwrite, so run twice is okey.
    parser.add_argument("--overwrite",
        help="force overwrite exist image file",
        action='store_true')

    args = parser.parse_args()

    image_file_in = args.input
    image_file_out = image_file_in
    
    if not args.output is None:
        image_file_out = args.output

    print("Open font:", image_file_in)
    print("Save path:", image_file_out)

    if not exists(image_file_in):
        print("image file not found:", args.input)
    else:
        img_raw = Image.open(image_file_in)

        # force convert to RGB
        img_rgb = Image.new("RGB", img_raw.size, (255, 255, 255))
        img_rgb.paste(img_raw)
        
        original_value = (args.from_r,args.from_g,args.from_b)
        target_value = (args.to_r,args.to_g,args.to_b)

        img_rgb = changeColor(img_rgb, original_value, target_value)
        
        if args.resize_canvas_size:
            img_rgb = img_rgb.resize( (args.resize_canvas_size, args.resize_canvas_size), Image.ANTIALIAS )
        img_rgb.save(image_file_out)


if __name__ == '__main__':
    main()
