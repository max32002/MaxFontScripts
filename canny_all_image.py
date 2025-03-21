#!/usr/bin/env python3
#encoding=utf-8

import cv2
import os
import argparse
import logging

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff'}

def canny_all(source_folder, width, output_folder):
    """
    對指定資料夾中的所有圖像執行 Canny 邊緣檢測。

    Args:
        source_folder (str): 輸入資料夾路徑。
        width (int): 輸出圖像的寬度，如果為 0，則不調整大小。
        output_folder (str): 輸出資料夾路徑。
    """
    file_count = 0
    image_count = 0
    convert_count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        file_count += 1

        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension.lower()
            if file_extension in IMG_EXTENSIONS:
                image_count += 1
                output_path = os.path.join(output_folder, filename)

                try:
                    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        logging.warning(f"Failed to read image: {file_path}")
                        continue

                    if width > 0:
                        real_h, real_w = img.shape[:2]
                        if real_w != width:
                            ratio = width / real_w
                            height = int(real_h * ratio)
                            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

                    edges = cv2.Canny(img, threshold1=100, threshold2=200)
                    cv2.imwrite(output_path, edges)
                    convert_count += 1
                    logging.info(f"Processed: {filename}")

                except Exception as e:
                    logging.error(f"Error processing {filename}: {e}")

        if file_count % 1000 == 0:
            logging.info(f"Processed {file_count} files")

    logging.info(f"All file count: {file_count}")
    logging.info(f"Image file count: {image_count}")
    logging.info(f"Converted image count: {convert_count}")

def cli():
    """解析命令行參數。"""
    parser = argparse.ArgumentParser(description="Resize and apply Canny edge detection to images in a directory.")
    parser.add_argument("--input", type=str, help="Input folder", required=True)
    parser.add_argument("--output", type=str, default=".", help="Output folder (default: current directory)")
    parser.add_argument('--width', type=int, default=0, help="Size of your output image, do nothing when set to 0")

    args = parser.parse_args()

    # 配置 logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    canny_all(args.input, args.width, args.output)

if __name__ == "__main__":
    cli()