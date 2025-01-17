#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import exists

from PIL import Image
import numpy as np
import cv2
import argparse

def anti_aliasing(image, strength=2):
    """使用高斯模糊來減少鋸齒效果"""
    ksize = max(1, strength * 2 + 1)  # 確保奇數大小的核心
    blurred = cv2.GaussianBlur(image, (ksize, ksize), 0)
    return blurred

def main():
    parser = argparse.ArgumentParser(description='anti aliasing')
    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default="output.png",
        type=str)

    parser.add_argument("--strength",
        help="鋸齒效果, from: 0 to N",
        default=2,
        type=int)

    parser.add_argument("--threshold",
        help="binary threshold value",
        default=127,
        type=int)

    args = parser.parse_args()

    if not exists(args.input):
        print("image file not found:", args.input)
    else:
        # 讀取影像
        image = cv2.imread(args.input)

        # 應用去鋸齒
        img_rgb = anti_aliasing(image, args.strength)

        # to binary
        ret, img_rgb = cv2.threshold(img_rgb, args.threshold, 255, cv2.THRESH_BINARY)

        # conver to gray
        #img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # 儲存結果
        cv2.imwrite(args.output, img_rgb)
        print(f"去鋸齒處理完成，結果已儲存至 {args.output}")

if __name__ == '__main__':
    main()
