#!/usr/bin/env python3
# encoding=utf-8
import shutil
import argparse
from pathlib import Path

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff', '.svg'}

def parse_range(range_str, base=16):
    if not range_str or ',' not in range_str.replace('-', ',').replace('~', ','):
        return set()
    try:
        parts = range_str.replace('-', ',').replace('~', ',').split(',')
        start, end = int(parts[0], base), int(parts[1], base)
        return set(range(start, end + 1))
    except (ValueError, IndexError):
        print(f"解析範圍失敗: {range_str}")
        return set()

def copy_out(args):
    source_dir = Path(args.input)
    output_dir = Path(args.output)
    
    # 建立目標字元集
    target_unicode_set = {ord(c) for c in args.string}
    
    if args.file and Path(args.file).exists():
        with open(args.file, 'r', encoding='utf-8') as f:
            file_content = ''.join(line.strip() for line in f)
            target_unicode_set.update(ord(c) for c in file_content)

    target_unicode_set.update(parse_range(args.range, 16))
    target_unicode_set.update(parse_range(args.range_int, 10))

    if not source_dir.is_dir():
        print("來源路徑不是資料夾")
        return

    # 掃描來源檔案
    source_files = {}
    for f in source_dir.iterdir():
        if f.is_file() and f.suffix.lower() in IMG_EXTENSIONS:
            name = f.stem
            if name.isnumeric():
                code = int(name)
                if 0 < code < 0x110000:
                    source_files[code] = f

    # 比對並複製
    common_codes = target_unicode_set & set(source_files.keys())
    
    print(f"來源總數: {len(source_files)}")
    print(f"目標需求: {len(target_unicode_set)}")
    print(f"匹配總數: {len(common_codes)}")

    if not common_codes:
        print("沒有找到匹配的字型圖片")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    copy_count = 0
    conflict_count = 0

    for code in common_codes:
        src_path = source_files[code]
        dst_path = output_dir / src_path.name
        
        if dst_path.exists():
            print(f"衝突路徑: {dst_path}")
            conflict_count += 1
            
        shutil.copy2(src_path, dst_path)
        copy_count += 1

    print(f"完成。複製數量: {copy_count}, 衝突數量: {conflict_count}")

def cli():
    parser = argparse.ArgumentParser(description="從資料夾中篩選並複製特定編碼的圖片檔案")
    parser.add_argument("input", help="輸入資料夾路徑")
    parser.add_argument("--string", "-s", default="", help="目標字串")
    parser.add_argument("--file", "-f", default="", help="包含目標字串的文字檔")
    parser.add_argument("--range", "-r", default="", help="Unicode 16進位範圍 (如 4E00-4E10)")
    parser.add_argument("--range_int", "-int", default="", help="Unicode 10進位範圍")
    parser.add_argument("--output", "-o", default="output", help="輸出資料夾")
    parser.add_argument("--mode", "-m", default="unicode_image", help="運作模式")

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()