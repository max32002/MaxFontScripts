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
from tqdm import tqdm

# --- Potrace 參數預設值設定 ---
POTRACE_PRESETS = {
    "roundcap":    ["-a", "1.2", "-t", "2", "-O", "0.2", "-u", "10"], # 圓體 (ZenMaru)
    "squarecap":   ["-a", "1.0", "-t", "2", "-O", "0.2", "-u", "10"], # 黑體 (Noto Sans), potrace defalut
    "serif":       ["-a", "0.8", "-t", "1", "-O", "0.1", "-u", "10"], # 襯線 (Noto Serif/明體)
    "calligraphy": ["-a", "0.8", "-t", "3", "-O", "0", "-u", "10"],   # 毛筆 (保留墨跡細節)
    "pixel":       ["-a", "0",   "-t", "0", "-O", "0", "-u", "10"],   # 像素 (完全直角)
    "decorative":  ["-a", "0.9", "-t", "1", "-O", "0.1", "-u", "10"], # 藝術裝飾 (細節豐富)
    "test":        ["-a", "0", "-t", "0", "-O", "0", "-u", "1"]     # for test
}

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

def process_single_file(binray_path, input_path, output_folder, cwd, potrace_args):
    """
    處理單一檔案：轉換 PBM -> Potrace SVG -> 清理。
    potrace_args: 從預設模式中帶入的參數清單
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

        # 組合指令
        cmd = []
        if 'potrace' in binray_path:
            cmd = [
                binray_path, str(source_to_trace),
                "-s",
                "-b", "svg",
                "-o", str(output_path)
            ] + potrace_args

        if 'vtracer' in binray_path:
            cmd = [
                binray_path, 
                "--input", str(source_to_trace),
                "--output", str(output_path),
                "--colormode", "bw",
                "--preset", "bw",
                "-m", "spline"
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
    binary_path = args.binary
    cwd = pathlib.Path(args.cwd) if args.cwd else pathlib.Path.cwd()

    # 取得對應的 potrace 參數
    selected_args = POTRACE_PRESETS.get(args.stroke_cap, POTRACE_PRESETS["roundcap"])
    logging.info(f"Using Mode: {args.stroke_cap} | Args: {' '.join(selected_args)}")

    if not shutil.which(binary_path):
        logging.error(f"binary not found: {binary_path}")
        return

    if not from_folder.is_dir():
        logging.error(f"Input folder not found: {from_folder}")
        return

    to_folder.mkdir(parents=True, exist_ok=True)
    all_files = [f for f in from_folder.iterdir() if f.is_file()]

    max_workers = 1 if args.single_thread else None

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_file, binary_path, f, to_folder, cwd, selected_args)
            for f in all_files
        ]

        with tqdm(total=len(futures), desc="Processing", unit="file", dynamic_ncols=True) as pbar:
            for future in concurrent.futures.as_completed(futures):
                status_code, message = future.result()

                if status_code == 0:
                    pbar.set_postfix(file=message)
                elif status_code == 2:
                    tqdm.write(f"ERROR: {message}")

                pbar.update(1)

    logging.info("Task finished.")

def cli():
    parser = argparse.ArgumentParser(description="Batch convert images to SVG with specific stroke presets.")
    parser.add_argument("--input", "-i", required=True, help="Source folder")
    parser.add_argument("--output", "-o", help="Target folder")
    parser.add_argument("--single_thread", action="store_true", help="Single thread mode")
    parser.add_argument("--cwd", help="Working directory", default=None)
    parser.add_argument("--binary", help="Potrace/VTracer/AutoTrace/Inkscape/osra path", default="vtracer")

    # 新增 stroke_cap 參數
    parser.add_argument(
            "--stroke_cap", "-c",
            choices=["roundcap", "squarecap", "serif", "calligraphy", "pixel", "decorative", "test"],
            default="roundcap",
            help=(
                "Preset style: "
                "roundcap (ZenMaru), "
                "squarecap (NotoSans), "
                "serif (NotoSerif/Ming), "
                "calligraphy (Brush), "
                "pixel (DotFont), "
                "decorative (Artistic)"
            )
        )
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()