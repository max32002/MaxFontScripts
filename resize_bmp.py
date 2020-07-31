#!/usr/bin/env python3
#encoding=utf-8

import os
import glob

# for read bmp.
from PIL import Image

def resize(filename, width):
    ret = False
    #im = Image.open( "U_36935.bmp" )
    im = Image.open( filename )
    #print(im.format, im.size, im.mode)
    #width = 1000
    ratio = float(width)/im.size[0]
    height = int(im.size[1]*ratio)
    # Image resizing methods resize() and thumbnail() take a resample argument, 
    # which tells which filter should be used for resampling. 
    # Possible values are: 
    # PIL.Image.NEAREST, PIL.Image.BILINEAR, PIL.Image.BICUBIC and PIL.Image.ANTIALIAS. 
    # Almost all of them were changed in this version.
    if im.size[0] != width:
        nim = im.resize( (width, height), Image.ANTIALIAS )
        #print(nim.size)
        #nim.save( "resized.jpg" )
        nim.save(filename)
        ret = True

    return ret

def convert(path, width):
    readonly = True     #debug
    readonly = False    #online

    file_count=0
    convert_count=0

    filename_pattern = path + "/*.bmp"
    for name in glob.glob(filename_pattern):
        file_count+=1
        #print(file_count,":convert filename:", name)

        # debug single index.
        #if not idx == 19:
            #continue

        #if idx <= 27700:
            #continue

        is_convert = False
        is_convert = resize(name,width)
        if is_convert:
            convert_count+=1
            #print("convert list:", name)
        #break
        if file_count % 1000 == 0:
            print("Processing:", file_count)

    print("File count:", file_count)
    print("Resize count:", convert_count)


    return file_count


if __name__ == '__main__':
    import sys

    default_width = 1000

    argument_count = 2
    if len(sys.argv)==argument_count:
        bmp_path = sys.argv[1]
        if len(bmp_path) > 0:
            convert(bmp_path, default_width)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))

