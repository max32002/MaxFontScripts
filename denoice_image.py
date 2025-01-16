#!/usr/bin/env python3
#encoding=utf-8

import cv2
import numpy as np
import argparse

def denoise_image(input_path, output_path):
    # 讀取圖片
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f"無法讀取圖片: {input_path}")
        return

    # 轉換為灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用高斯模糊去除噪點
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用雙邊濾波保留邊緣細節
    denoised = cv2.bilateralFilter(image, 9, 75, 75)

    # 另存為新的圖檔
    cv2.imwrite(output_path, denoised)
    print(f"去雜點圖片已儲存至: {output_path}")

    # 顯示處理結果
    #cv2.imshow('Original', image)
    #cv2.imshow('Denoised', denoised)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def denoise_and_antialias(input_path, output_path):
    # 讀取圖片
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f"無法讀取圖片: {input_path}")
        return

    # 轉換為灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 去除雜點 (高斯模糊 + 雙邊濾波)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    denoised = cv2.bilateralFilter(image, 9, 75, 75)

    # 邊緣檢測
    edges = cv2.Canny(blurred, 50, 150)

    # 形態學閉運算來平滑邊緣 (去鋸齒)
    kernel = np.ones((3, 3), np.uint8)
    smoothed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 超分辨率放大再縮小 (Lanczos 插值去鋸齒)
    h, w = denoised.shape[:2]
    upscaled = cv2.resize(denoised, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)
    antialiased = cv2.resize(upscaled, (w, h), interpolation=cv2.INTER_LANCZOS4)

    # 另存為新的圖檔
    cv2.imwrite(output_path, antialiased)
    print(f"去雜點 & 抗鋸齒圖片已儲存至: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="去除圖片雜點並另存為新檔案")
    parser.add_argument("--input", type=str, default=None, help="輸入圖片的路徑")
    parser.add_argument("--output", type=str, default=None, help="輸出圖片的路徑")
    parser.add_argument('--antialias', type=int, default=1)
    args = parser.parse_args()

    # overwrite input
    if args.output is None:
        args.output = args.input

    if not args.input is None:
        if args.antialias == 1:
            print("denoise + anti-alias")
            denoise_and_antialias(args.input, args.output)
        else:
            print("denoise")
            denoise_image(args.input, args.output)
    else:
        # 使用方法
        print("python script.py noisy_image.jpg cleaned_image.jpg")
