#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

def process_file(file_path: Path, pattern: re.Pattern, replacement: str):
    temp_file = file_path.with_suffix(file_path.suffix + ".tmp")
    
    try:
        modified = False
        with open(file_path, 'r', encoding='utf-8') as fin, \
             open(temp_file, 'w', encoding='utf-8') as fout:
            for line in fin:
                new_line = pattern.sub(replacement, line)
                if new_line != line:
                    modified = True
                fout.write(new_line)
        
        if modified:
            temp_file.replace(file_path)
            print(f"[\x1b[32m已修改\x1b[0m] {file_path}")
        else:
            temp_file.unlink()
            print(f"[無變動] {file_path}")
            
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"[跳過] {file_path} (原因: {e})")
        if temp_file.exists():
            temp_file.unlink()

def main():
    parser = argparse.ArgumentParser(description="正則表達式批量替換工具")
    parser.add_argument("path", help="目標路徑")
    parser.add_argument("pattern", help="正則表達式")
    parser.add_argument("replacement", help="替換字串")
    parser.add_argument("filter", nargs="?", default="*", help="檔案過濾 (預設: *)")
    parser.add_argument("-r", "-R", "--recursive", action="store_true", help="遞迴掃描子資料夾")

    args = parser.parse_args()

    base_path = Path(args.path)
    try:
        pattern = re.compile(args.pattern)
    except re.error as e:
        print(f"正則表達式語法錯誤: {e}")
        return

    if base_path.is_file():
        process_file(base_path, pattern, replacement)
    elif base_path.is_dir():
        # 根據是否遞迴選擇 glob 或 rglob
        files = base_path.rglob(args.filter) if args.recursive else base_path.glob(args.filter)
        
        print(f"模式: {'遞迴' if args.recursive else '僅當前目錄'}")
        for file_path in files:
            if file_path.is_file():
                process_file(file_path, pattern, args.replacement)
    else:
        print(f"錯誤: 路徑不存在 '{base_path}'")

if __name__ == '__main__':
    main()