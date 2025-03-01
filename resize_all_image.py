#!/usr/bin/env python3
#encoding=utf-8

import os
import glob
from PIL import Image
import argparse

IMG_EXTENSIONS = ['.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.BMP', '.TIF', '.TIFF']

def is_image_file(filename):
    _ , file_extension = os.path.splitext(filename)
    file_extension = file_extension.upper()
    return file_extension in IMG_EXTENSIONS

def resize_one(filename, width, target):
    ret = False
    im = Image.open(filename)
    ratio = float(width)/im.size[0]
    height = int(im.size[1]*ratio)
    if im.size[0] != width and ratio > 0.0:
        nim = im.resize( (width, height), Image.BILINEAR )
        nim.save(target)
        ret = True
    return ret

def resize_all(source_folder, width, output_folder):
    file_count = 0
    image_count = 0
    convert_count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_folder_list = os.listdir(source_folder)
    for filename in output_folder_list:
        file_count += 1
        if is_image_file(filename): 
            image_count += 1
            #print("image file name", filename)
            
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(output_folder, filename)

            is_convert = False
            if width > 0:
                is_convert = resize_one(source_path, width, target_path)

            if is_convert:
                convert_count+=1
                #print("convert list:", name)
            #break
            if file_count % 1000 == 0:
                print("Processing:", file_count)
    print("All file count:", file_count)
    print("Image file count:", image_count)
    print("Resize count:", convert_count)
    return file_count

def cli():
    parser = argparse.ArgumentParser(description="resize all image under directory")
    parser.add_argument("--input", type=str, help="input folder", required=True)
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument('--width', type=int, default=0, help="size of your output image")
    
    args = parser.parse_args()
    resize_all(args.input, args.width, args.output)

if __name__ == "__main__":
    cli()
