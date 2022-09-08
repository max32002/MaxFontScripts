#!/usr/bin/env python3
#encoding=utf-8

import os

# for read bmp.
from PIL import Image

import argparse

def resize(source, target, width):
    import PIL.Image
    if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
        PIL.Image.Resampling = PIL.Image
    # Now PIL.Image.Resampling.BICUBIC is always recognized.

    ret = False
    im = Image.open(source)
    ratio = float(width)/im.size[0]
    height = int(im.size[1]*ratio)
    # Image resizing methods resize() and thumbnail() take a resample argument, 
    # which tells which filter should be used for resampling. 
    # Possible values are: 
    # PIL.Image.NEAREST, PIL.Image.BILINEAR, PIL.Image.BICUBIC and PIL.Resampling.LANCZOS. 
    # Almost all of them were changed in this version.
    if im.size[0] != width:
        nim = im.resize( (width, height), PIL.Image.Resampling.BICUBIC )

        print("image.mode:", nim.mode)
        #print("image.getbands():", nim.getbands())

        split_tup = os.path.splitext(target)
        file_extension = split_tup[1].upper()

        need_convert_rgb = False
        if file_extension == '.JPG' or file_extension == '.JPEG':
            need_convert_rgb = True

        if file_extension == '.BMP':
            need_convert_rgb = True

        if need_convert_rgb:
            # convert to white
            if nim.mode == "RGBA":
                background = Image.new("RGB", nim.size, (255, 255, 255))
                background.paste(nim, mask=nim.split()[3])
                nim = background

            #nim = nim.convert('RGB')

        nim.save(target)
        ret = True

    return ret

def t_or_f(arg):
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
       return True
    elif 'FALSE'.startswith(ua):
       return False
    else:
       pass  #error condition maybe?

def convert(args):

    source, target = args.input, args.output
    width = args.width
    overwrite = t_or_f(args.overwrite)
    mode = args.mode

    if target is None:
        target = source

    pass_check = True
    if pass_check:
        if not os.path.exists(source):
            pass_check = False
            print("Error: source image[%s] not exists." % (source))

    if pass_check:
        if width <= 0:
            pass_check = False
            print("Error: size format wrong")

    # rename target filename.
    if pass_check:
        if not overwrite:
            if os.path.exists(target):
                # this will return a tuple of root and extension
                split_tup = os.path.splitext(target)
                print(split_tup)
                 
                # extract the file name and extension
                file_name = split_tup[0]
                file_extension = split_tup[1]
                 
                #print("File Name: ", file_name)
                #print("File Extension: ", file_extension)
                target = "%s_x%d%s" % (file_name, width, file_extension)

    print("source:", source)
    print("target:", target)
    print("new width:", width)
    print("overwrite:", overwrite)
    print("mode:", mode)

    if pass_check:
        is_convert = False
        is_convert = resize(source, target, width)


def cli():
    parser = argparse.ArgumentParser(
            description="resize image to new width")

    parser.add_argument("--input",
        help="source image",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="target image",
        type=str)

    parser.add_argument("--width",
        help="new target width",
        required=True,
        type=int)

    parser.add_argument("--mode",
        help="resize mode",
        default='BICUBIC',
        choices=['NEAREST','BILINEAR','BICUBIC','LANCZOS'],
        type=str)

    parser.add_argument("--overwrite",
        help="overwrite target file",
        default='True',
        type=str)

    args = parser.parse_args()
    convert(args)


if __name__ == "__main__":
    cli()

