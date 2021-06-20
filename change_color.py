#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import exists

import numpy as np
from PIL import Image
import argparse


def changeColor(im, from_rgb_value, to_rgb_value):
    data = np.array(im)

    r1, g1, b1 = from_rgb_value
    r2, g2, b2 = to_rgb_value

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

    # allow fuzzy mode.
    parser.add_argument("--fuzziness",
        help="select more colors",
        default=None,
        type=int)

    args = parser.parse_args()

    image_file_in = args.input
    image_file_out = image_file_in
    fuzziness = args.fuzziness
    
    if not args.output is None:
        image_file_out = args.output

    #print("Open font:", image_file_in)
    #print("Save path:", image_file_out)

    cnt = 0
    if not exists(image_file_in):
        print("image file not found:", args.input)
    else:
        img_raw = Image.open(image_file_in)

        # force convert to RGB
        img_rgb = Image.new("RGB", img_raw.size, (255, 255, 255))
        img_rgb.paste(img_raw)
        
        from_rgb_value = (args.from_r,args.from_g,args.from_b)
        to_rgb_value = (args.to_r,args.to_g,args.to_b)

        if not fuzziness:
            # only replace 1 color.
            img_rgb = changeColor(img_rgb, from_rgb_value, to_rgb_value)
        else:
            # fuzzy mode.
            if fuzziness > 0:
                #print("fuzziness: %d" % (fuzziness))
                #print("from RGB color: %d,%d,%d" % (args.from_r,args.from_g,args.from_b))
                #print("to RGB color: %d,%d,%d" % (args.to_r,args.to_g,args.to_b))
                
                for direction in range(-1,2,2):
                    #print("direction: %d" % (direction))
                    for increase_value in range(fuzziness):
                        #print("increase_value: %d" % (increase_value))
                        # PS: not support RGB mode, for GRAY mode now.
                        target_r = args.from_r + (direction * (increase_value+1))
                        if target_r <=0:
                            target_r = 0
                        if target_r >=255:
                            target_r = 255

                        target_g = args.from_g + (direction * (increase_value+1))
                        if target_g <=0:
                            target_g = 0
                        if target_g >=255:
                            target_g = 255

                        target_b = args.from_b + (direction * (increase_value+1))
                        if target_b <=0:
                            target_b = 0
                        if target_b >=255:
                            target_b = 255

                        #print("target_r: %d" % (target_r))
                        #print("target_g: %d" % (target_g))
                        #print("target_b: %d" % (target_b))
                        from_rgb_value = (target_r, target_g, target_b)
                        img_rgb = changeColor(img_rgb, from_rgb_value, to_rgb_value)
        
        if args.resize_canvas_size:
            img_rgb = img_rgb.resize( (args.resize_canvas_size, args.resize_canvas_size), Image.ANTIALIAS )
        img_rgb.save(image_file_out)
        cnt += 1

    #print("Convert %d images." % (cnt))


if __name__ == '__main__':
    main()
