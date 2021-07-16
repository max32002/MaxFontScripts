#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import exists

from PIL import Image
import numpy as np
import cv2
import argparse

def blur(image_file_in, image_file_out):
    # PIL
    #img_raw = Image.open(image_file_in)

    # OpenCV
    '''
    cv2.IMREAD_COLOR
        此為預設值，這種格式會讀取 RGB 三個 channels 的彩色圖片，而忽略透明度的 channel。
    cv2.IMREAD_GRAYSCALE
        以灰階的格式來讀取圖片。
    cv2.IMREAD_UNCHANGED
        讀取圖片中所有的 channels，包含透明度的 channel。
    '''
    img_rgb = cv2.imread(image_file_in, cv2.IMREAD_COLOR)

    # PIL: force convert to RGB
    #img_rgb = Image.new("RGB", img_raw.size, (255, 255, 255))
    #img_rgb.paste(img_raw)
    
    # PIL
    #img_rgb.save(image_file_out)


    # denoise
    img_rgb = cv2.fastNlMeansDenoisingColored(img_rgb,None,10,10,7,21)

    # blur...
    #img_rgb = cv2.blur(img_rgb, (5, 5))
    img_rgb = cv2.blur(img_rgb, (10, 10))

    img_rgb = cv2.fastNlMeansDenoisingColored(img_rgb,None,10,10,7,21)
    #img_rgb = cv2.GaussianBlur(img_rgb, (5, 5), 0)
    #img_rgb = cv2.medianBlur(img_rgb,5)
    ret, img_rgb = cv2.threshold(img_rgb, 127, 255, cv2.THRESH_BINARY)

    #img_rgb = cv2.blur(img_rgb, (10, 10))
    img_rgb = cv2.GaussianBlur(img_rgb, (5, 5), 0)
    ret, img_rgb = cv2.threshold(img_rgb, 127, 255, cv2.THRESH_BINARY)

    # OpenCV
    cv2.imwrite(image_file_out, img_rgb)

def main():
    parser = argparse.ArgumentParser(description='anti aliasing')
    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default=None,
        type=str)

    args = parser.parse_args()

    image_file_in = args.input
    image_file_out = image_file_in
    
    if not args.output is None:
        image_file_out = args.output

    #print("Open font:", image_file_in)
    #print("Save path:", image_file_out)

    if not exists(image_file_in):
        print("image file not found:", args.input)
    else:
        blur(image_file_in, image_file_out)

if __name__ == '__main__':
    main()
