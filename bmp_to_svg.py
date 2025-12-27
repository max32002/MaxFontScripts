#!/usr/bin/env python3
import argparse
import subprocess
import concurrent.futures
import pathlib
import shutil
import logging
import cv2
import tempfile
import os
from tqdm import tqdm  # 引入 tqdm

# --- 日誌與進度條相容設定 ---
class SimpleColorFormatter(logging.Formatter):
    COLORS = {
        'INFO': "\x1b[32mINFO\x1b[0m",
        'WARNING': "\x1b[33mWARNING\x1b[0m",
        'ERROR': "\x1b[31mERROR\x1b[0m",
        'DEBUG': "\x1b[36mDEBUG\x1b[0m",
    }

    def format(self, record):
        level_name = self.COLORS.get(record.levelname, record.levelname)
        return f"{level_name}: {record.getMessage()}"

def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(SimpleColorFormatter())
        logger.addHandler(handler)

# --- 核心處理邏輯 ---

def process_single_file(potrace_path, input_path, output_folder, cwd):
    """
    處理單一檔案：轉換 PBM -> Potrace SVG -> 清理。
    傳回值：(狀態碼, 訊息) 狀態碼 0:成功, 1:跳過, 2:錯誤
    """
    supported_native = {'.bmp', '.pbm', '.pgm', '.ppm'}
    opencv_supported = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp'}
    
    ext = input_path.suffix.lower()
    temp_pbm = None
    output_path = output_folder / f"{input_path.stem}.svg"

    try:
        if ext in supported_native:
            source_to_trace = input_path
        elif ext in opencv_supported:
            fd, temp_path = tempfile.mkstemp(suffix='.pbm')
            os.close(fd)
            temp_pbm = pathlib.Path(temp_path)
            
            image = cv2.imread(str(input_path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                return 2, f"Read Error: {input_path.name}"
            cv2.imwrite(str(temp_pbm), image)
            source_to_trace = temp_pbm
        else:
            return 1, f"Skip: {input_path.name}"

        cmd = [
            potrace_path, '-b', 'svg', '-u', '60',
            str(source_to_trace), '-o', str(output_path),
        ]
        
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)
        return 0, input_path.name

    except Exception as e:
        return 2, f"Fail: {input_path.name} ({str(e)})"
    
    finally:
        if temp_pbm and temp_pbm.exists():
            temp_pbm.unlink()

def main(args):
    setup_logging()
    
    from_folder = pathlib.Path(args.input)
    to_folder = pathlib.Path(args.output) if args.output else from_folder
    potrace_path = args.potrace
    cwd = pathlib.Path(args.cwd) if args.cwd else pathlib.Path.cwd()

    if not shutil.which(potrace_path):
        logging.error(f"Potrace not found: {potrace_path}")
        return

    if not from_folder.is_dir():
        logging.error(f"Input folder not found: {from_folder}")
        return

    to_folder.mkdir(parents=True, exist_ok=True)
    all_files = [f for f in from_folder.iterdir() if f.is_file()]
    
    max_workers = 1 if args.single_thread else None
    
    # 使用 tqdm 建立進度條
    # total: 總量, desc: 左側標題, unit: 單位
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_file, potrace_path, f, to_folder, cwd)
            for f in all_files
        ]
        
        with tqdm(total=len(futures), desc="Processing", unit="file", dynamic_ncols=True) as pbar:
            for future in concurrent.futures.as_completed(futures):
                status_code, message = future.result()
                
                if status_code == 0:
                    # 成功處理：更新進度條右側的小字 (postfix)
                    pbar.set_postfix(file=message)
                elif status_code == 2:
                    # 出錯時：使用 tqdm.write 避免破壞進度條佈局
                    tqdm.write(f"ERROR: {message}")
                
                pbar.update(1) # 跳下一格

    logging.info("Task finished.")

def cli():
    parser = argparse.ArgumentParser(description="Batch convert images to SVG with progress bar.")
    parser.add_argument("--input", "-i", required=True, help="Source folder")
    parser.add_argument("--output", "-o", help="Target folder")
    parser.add_argument("--single_thread", action="store_true", help="Single thread mode")
    parser.add_argument("--cwd", help="Working directory", default=None)
    parser.add_argument("--potrace", help="Potrace path", default="potrace")

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()