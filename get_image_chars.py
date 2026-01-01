#!/usr/bin/env python3
#encoding=utf-8
import argparse
from pathlib import Path

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.gif', '.tif', '.tiff', '.svg', '.kra', '.psd'}

def save_set_to_file(sorted_set, filename_output):
    try:
        with open(filename_output, 'w', encoding='utf-8') as f:
            full_text = "".join(chr(item) for item in sorted_set)
            f.write(full_text)
    except Exception as e:
        print(f"寫入檔案時發生錯誤: {e}")

def main(args):
    source_folder = Path(args.input)
    if not source_folder.is_dir():
        print("輸入的路徑不是資料夾")
        return

    source_unicode_set = set()

    for file_path in source_folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in IMG_EXTENSIONS:
            char_string = file_path.stem
            
            try:
                if args.filename_source == 'unicode_int':
                    char_int = int(char_string)
                elif args.filename_source == 'unicode_hex':
                    char_int = int(char_string, 16)
                else:
                    if len(char_string) > 0:
                        char_int = ord(char_string[0])
                    else:
                        continue

                if 0 <= char_int < 0x110000:
                    source_unicode_set.add(char_int)
            except ValueError:
                continue

    if source_unicode_set:
        sorted_set = sorted(list(source_unicode_set))
        
        # 判斷輸出檔名
        if args.output:
            filename_output = args.output
        else:
            # 如果 user 沒輸入，使用資料夾名稱加上 .txt
            filename_output = f"{source_folder.name}.txt"

        save_set_to_file(sorted_set, filename_output)

        print(f"輸入目錄: {source_folder}")
        print(f"輸出檔案: {filename_output}")
        print(f"解析格式: {args.filename_source}")
        print(f"字元數量: {len(sorted_set)}")
    else:
        print("資料夾內沒有符合條件的圖片檔案或解析失敗")

def cli():
    parser = argparse.ArgumentParser(description="從圖片檔名獲取字型清單")
    parser.add_argument("input", help="輸入目錄路徑")
    parser.add_argument("--output", "-o", help="輸出文件路徑", default=None)
    parser.add_argument("--filename_source", "-f", 
                        choices=['char', 'unicode_hex', 'unicode_int'], 
                        default="unicode_int", 
                        help="檔名解析格式")

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()
