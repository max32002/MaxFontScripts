#!/usr/bin/env python3
#encoding=utf-8

import cv2
import numpy as np
import os
import argparse

IMG_EXTENSIONS = ['.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.BMP', '.TIF', '.TIFF']

def is_image_file(filename):
    _ , file_extension = os.path.splitext(filename)
    file_extension = file_extension.upper()
    return file_extension in IMG_EXTENSIONS

def canny_all(source_folder, width, output_folder):
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
            output_path = os.path.join(output_folder, filename)

            img = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
            
            if width > 0:
                real_h = 0
                real_w = 0
                if len(img.shape) == 2:
                    real_h, real_w = img.shape
                if len(img.shape) == 3:
                    real_h, real_w, _ = img.shape

                ratio = float(width)/real_w
                height = int(real_h*ratio)
                if real_w != width and ratio > 0.0:
                    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

            # 使用 Canny 邊緣檢測
            edges = cv2.Canny(img, threshold1=100, threshold2=200)
            cv2.imwrite(output_path, edges)

            if file_count % 1000 == 0:
                print("Processing:", file_count)
    print("All file count:", file_count)
    print("Image file count:", image_count)
    return file_count

def cli():
    parser = argparse.ArgumentParser(description="resize all image under directory")
    parser.add_argument("--input", type=str, help="input folder", required=True)
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument('--width', type=int, default=0, help="size of your output image, do nothing when set to 0")
    
    args = parser.parse_args()
    canny_all(args.input, args.width, args.output)

if __name__ == "__main__":
    cli()


