#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def process_file(file_path: Path, pattern: re.Pattern, replacement: str):
    """使用正則表達式處理單一檔案。"""
    temp_file = file_path.with_suffix(file_path.suffix + ".tmp")
    
    try:
        modified = False
        with open(file_path, 'r', encoding='utf-8') as fin, \
             open(temp_file, 'w', encoding='utf-8') as fout:
            for line in fin:
                # 使用 re.sub 進行正則替換
                new_line = pattern.sub(replacement, line)
                if new_line != line:
                    modified = True
                fout.write(new_line)
        
        if modified:
            temp_file.replace(file_path)
            print(f"[已修改] {file_path}")
        else:
            temp_file.unlink() # 若無變動則刪除暫存檔，保持原檔案不變
            print(f"[無變動] {file_path}")
            
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"[跳過] {file_path} (原因: {e})")
        if temp_file.exists():
            temp_file.unlink()

def main():
    if len(sys.argv) < 4:
        print("用法: python script.py <路徑> <正則表達式> <替換字串> [檔案過濾, 預設 *]")
        print("範例: python script.py ./src \"v\d+\.\d+\" \"v1.0\" \"*.txt\"")
        sys.exit(1)

    base_path = Path(sys.argv[1])
    regex_pattern = sys.argv[2]
    replacement = sys.argv[3]
    file_filter = sys.argv[4] if len(sys.argv) > 4 else "*"

    try:
        # 預編譯正則表達式以提高效能
        pattern = re.compile(regex_pattern)
    except re.error as e:
        print(f"正則表達式語法錯誤: {e}")
        sys.exit(1)

    if base_path.is_file():
        process_file(base_path, pattern, replacement)
    elif base_path.is_dir():
        print(f"開始批次處理目錄: {base_path} (過濾條件: {file_filter})")
        # rglob 會遞迴搜尋所有子目錄
        for file_path in base_path.rglob(file_filter):
            if file_path.is_file():
                process_file(file_path, pattern, replacement)
    else:
        print(f"錯誤: 路徑不存在 '{base_path}'")

if __name__ == '__main__':
    main()

#使用範例
# * 簡單替換： python replace_string.py ./docs "Apple" "Orange"
# * 使用正則表達式（將所有版本號 v1, v2... 改為 v3）： python replace_string.py ./project "v\d+" "v3"
# * 僅針對特定副檔名（例如只改 .conf 檔）： python replace_string.py /etc "127.0.0.1" "0.0.0.0" "*.conf"