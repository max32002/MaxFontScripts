#!/usr/bin/env python3
import argparse
import os
import subprocess
import concurrent.futures
import platform
import pathlib
import shutil
import logging
import cv2

class SimpleColorFormatter(logging.Formatter):
    # 定義顏色碼
    COLORS = {
        'INFO': "\x1b[32mINFO\x1b[0m",
        'WARNING': "\x1b[33mWARNING\x1b[0m",
        'ERROR': "\x1b[31mERROR\x1b[0m",
        'DEBUG': "\x1b[36mDEBUG\x1b[0m",
    }

    def format(self, record):
        level_name = self.COLORS.get(record.levelname, record.levelname)
        return f"{level_name}: {record.getMessage()}"

# 套用設定
handler = logging.StreamHandler()
handler.setFormatter(SimpleColorFormatter())
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

# 設定日誌記錄
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(levelname).1s: %(message)s')

def check_potrace(potrace_path):
    """檢查 potrace 是否存在。如果不存在，則引發異常。"""
    if shutil.which(potrace_path) is None:
        raise FileNotFoundError(f"potrace not found at: {potrace_path}")

def convert_image_to_pbm(input_path, output_path):
    """使用 OpenCV 將圖像轉換為 PBM 格式。"""
    try:
        image = cv2.imread(str(input_path), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(str(output_path), image)
        logging.info(f"Converted {input_path} to PBM: {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error converting {input_path} to PBM: {e}")
        return False

def convert_image_to_svg(potrace_path, input_path, output_path, cwd):
    """將單個圖像檔案轉換為 SVG。"""
    cmd_arguments = [
        potrace_path,
        '-b', 'svg',
        '-u', '60',
        str(input_path),
        '-o', str(output_path),
    ]

    try:
        subprocess.run(cmd_arguments, cwd=cwd, check=True, capture_output=True)
        logging.info(f"Converted {input_path} to {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {input_path}: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        logging.error(f"potrace not found at {potrace_path}.")
        return False

def main(args):
    """主函數，用於批次轉換圖像檔案。"""

    from_folder = pathlib.Path(args.input)
    to_folder = pathlib.Path(args.output) if args.output else from_folder
    multi_thread = not args.single_thread
    cwd = pathlib.Path(args.cwd) if args.cwd else pathlib.Path.cwd()
    potrace_path = args.potrace

    logging.info(f"From folder: {from_folder}")
    logging.info(f"To folder: {to_folder}")
    logging.info(f"Working folder: {cwd}")
    logging.info(f"Using potrace: {potrace_path}")
    logging.info(f"Multi-thread: {multi_thread}")

    check_potrace(potrace_path)

    if not from_folder.exists() or not from_folder.is_dir():
        logging.error(f"Input folder not found: {from_folder}")
        return

    if not to_folder.exists():
        logging.info(f"Output folder not found, creating {to_folder}")
        to_folder.mkdir(parents=True, exist_ok=True)
    elif not to_folder.is_dir():
        logging.error(f"Output path is not a directory: {to_folder}")
        return

    supported_extensions = {'.bmp', '.pbm', '.pgm', '.ppm'}
    opencv_supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff'}
    image_files = [f for f in from_folder.iterdir() if f.is_file()]

    logging.info(f"Total files in from folder: {len(image_files)}")

    files_to_convert = []
    temp_pbm_files = []

    for image_file in image_files:
        if image_file.suffix.lower() in supported_extensions:
            files_to_convert.append(image_file)
        elif image_file.suffix.lower() in opencv_supported_extensions:
            temp_pbm_path = from_folder / f"{image_file.stem}.pbm"
            if convert_image_to_pbm(image_file, temp_pbm_path):
                files_to_convert.append(temp_pbm_path)
                temp_pbm_files.append(temp_pbm_path)
        else :
            logging.info(f"file: {image_file} is not supported.")

    if multi_thread:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(
                    convert_image_to_svg,
                    potrace_path,
                    image_file,
                    to_folder / f"{image_file.stem}.svg",
                    cwd,
                )
                for image_file in files_to_convert
            ]
            concurrent.futures.wait(futures)
    else:
        for image_file in files_to_convert:
            convert_image_to_svg(
                potrace_path,
                image_file,
                to_folder / f"{image_file.stem}.svg",
                cwd,
            )

    # 刪除臨時 PBM 檔案
    for temp_pbm_file in temp_pbm_files:
        temp_pbm_file.unlink()
        logging.info(f"Deleted temporary file: {temp_pbm_file}")

    logging.info("Conversion complete.")

def cli():
    """解析命令行參數。"""
    parser = argparse.ArgumentParser(
        description="Batch convert images to SVG using potrace."
    )
    parser.add_argument("--input", required=True, help="Source folder")
    parser.add_argument("--output", help="Target folder", default="")
    parser.add_argument("--single_thread", action="store_true", help="Run in single-thread mode")
    parser.add_argument("--cwd", help="Working directory", default=str(pathlib.Path.cwd()))
    parser.add_argument("--potrace", help="Path to potrace executable", default="potrace")

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()