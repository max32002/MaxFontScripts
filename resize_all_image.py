#!/usr/bin/env python3
# encoding=utf-8

import os
import glob
from PIL import Image
import argparse
from pathlib import Path

IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff']

def resize_one(source_path, target_path, width):
    try:
        with Image.open(source_path) as im:
            if im.size[0] == width:
                return False

            ratio = width / im.size[0]
            height = int(im.size[1] * ratio)
            nim = im.resize((width, height), Image.BILINEAR)
            nim.save(target_path)
            return True
    except (IOError, OSError) as e:
        print(f"Error processing {source_path}: {e}")
        return False

def resize_all(source_folder, width, output_folder):
    source_path = Path(source_folder)
    output_path = Path(output_folder)

    if not output_path.exists():
        output_path.mkdir(parents=True)

    file_count = 0
    image_count = 0
    convert_count = 0

    for ext in IMG_EXTENSIONS:
        for file_path in source_path.glob(f'*{ext}'):
            file_count += 1
            image_count += 1
            target_file_path = output_path / file_path.name
            if resize_one(file_path, target_file_path, width):
                convert_count += 1

            if file_count % 100 == 0:
                print(f"Processed {file_count} files...")

    print(f"All file count: {file_count}")
    print(f"Image file count: {image_count}")
    print(f"Resize count: {convert_count}")

def cli():
    parser = argparse.ArgumentParser(description="resize all image under directory")
    parser.add_argument("--input", type=str, help="input folder", required=True)
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument('--width', type=int, default=0, help="size of your output image")

    args = parser.parse_args()
    resize_all(args.input, args.width, args.output)

if __name__ == "__main__":
    cli()