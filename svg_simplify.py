#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import subprocess
import concurrent.futures
import shutil
import sys
from pathlib import Path
import logging

# 設定日誌格式
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_scour_installed():
    """檢查系統是否安裝了 scour 執行檔"""
    if shutil.which("scour") is None:
        logging.error("找不到 'scour' 指令。")
        logging.error("請先安裝 Scour: pip install scour")
        return False
    return True

def process_svg(file_info):
    """處理單個 SVG 檔案"""
    input_path, output_path = file_info
    
    cmd = [
        "scour", "-q",
        "-i", str(input_path),
        "-o", str(output_path),
        "--enable-viewboxing",
        "--enable-id-stripping",
        "--enable-comment-stripping",
        "--shorten-ids",
        "--indent=none"
    ]
    
    try:
        # check=True 會在指令失敗時拋出異常
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"轉換失敗 [{input_path.name}]: {e.stderr.decode().strip()}")
        return False

def run_batch_conversion(args):
    """主邏輯控制區"""
    src_dir = Path(args.input)
    dst_dir = Path(args.output) if args.output else src_dir

    if not src_dir.is_dir():
        logging.error(f"來源路徑不是有效的資料夾: {src_dir}")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)

    # 搜尋所有 .svg 檔案
    svg_files = list(src_dir.glob("*.svg"))
    if not svg_files:
        logging.info("資料夾中沒有 .svg 檔案。")
        return

    tasks = [(f, dst_dir / f.name) for f in svg_files]
    logging.info(f"開始優化 {len(tasks)} 個檔案 (並行度: {args.workers or '自動'})...")

    success_count = 0
    # 使用 ThreadPoolExecutor 進行並行處理
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(process_svg, tasks))
        success_count = sum(1 for r in results if r)

    logging.info("-" * 30)
    logging.info(f"任務完成！")
    logging.info(f"成功: {success_count}")
    logging.info(f"失敗: {len(tasks) - success_count}")

def main():
    parser = argparse.ArgumentParser(description="SVG 批次優化工具 (Scour 封裝)")
    parser.add_argument("--input", "-i", required=True, help="來源資料夾路徑")
    parser.add_argument("--output", "-o", help="輸出資料夾路徑 (預設蓋過原檔)")
    parser.add_argument("--workers", "-w", type=int, default=None, help="並行工作數量")
    
    args = parser.parse_args()

    # --- 核心檢查點 ---
    if not check_scour_installed():
        sys.exit(1) # 回傳非零狀態碼表示異常結束
    
    run_batch_conversion(args)

if __name__ == "__main__":
    main()