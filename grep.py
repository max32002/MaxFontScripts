import os
import collections
import argparse
import re

def output_text(text, file_handle=None):
    print(text)
    if file_handle:
        clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
        file_handle.write(clean_text + "\n")

def grep_context(file_path, keyword, before=2, after=2, out_f=None, ignore_case=False, no_line_number=False, highlight=False, use_regex=False):
    before_history = collections.deque(maxlen=before)
    after_count = 0
    found_any = False
    
    flags = re.IGNORECASE if ignore_case else 0
    pattern_str = keyword if use_regex else re.escape(keyword)
    
    try:
        pattern = re.compile(pattern_str, flags)
    except re.error:
        print(f"錯誤：無效的正規表示法 '{keyword}'")
        return

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                match = pattern.search(clean_line)
                
                if match:
                    if not found_any:
                        print(f"\n>>> 檔案: {file_path}")
                        found_any = True
                    
                    while before_history:
                        h_line = before_history.popleft()
                        prefix = "" if no_line_number else f"{line_num - len(before_history) - 1}: "
                        output_text(f"{prefix}{h_line}", out_f)
                    
                    display_line = clean_line
                    if highlight:
                        display_line = pattern.sub(r"\033[1;31m\g<0>\033[0m", clean_line)

                    prefix = "" if no_line_number else f"{line_num}* "
                    output_text(f"{prefix}{display_line}", out_f)
                    after_count = after
                elif after_count > 0:
                    prefix = "" if no_line_number else f"{line_num}: "
                    output_text(f"{prefix}{clean_line}", out_f)
                    after_count -= 1
                else:
                    before_history.append(clean_line)
    except Exception:
        pass

def search_directory(root_path, keyword, args, out_f=None):
    # 如果沒開啟遞迴，就把 os.walk 的 dirs 清空，讓它不往下走
    for root, dirs, files in os.walk(root_path):
        if not args.recursive:
            dirs.clear() 
            
        for file in files:
            if file.endswith(args.ext):
                full_path = os.path.join(root, file)
                grep_context(full_path, keyword, args.b, args.a, out_f, 
                             args.ignore_case, args.no_line_number, 
                             args.highlight, args.extended_regexp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="要搜尋的關鍵字或正規表示法")
    parser.add_argument("path", help="檔案路徑或資料夾路徑")
    parser.add_argument("-b", type=int, default=0, help="顯示前幾行")
    parser.add_argument("-a", type=int, default=0, help="顯示後幾行")
    parser.add_argument("-ext", default=".log", help="指定副檔名 (預設 .log)")
    parser.add_argument("-o", "--output", help="將結果輸出到指定檔案")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小寫")
    parser.add_argument("-n", "--no-line-number", action="store_true", help="不顯示行號")
    parser.add_argument("-l", "--highlight", action="store_true", help="高亮顯示關鍵字")
    parser.add_argument("-E", "--extended-regexp", action="store_true", help="支援擴展正規表示法")
    parser.add_argument("-r", "-R", "--recursive", action="store_true", help="遞迴搜尋子目錄")
    
    args = parser.parse_args()

    out_file = None
    if args.output:
        out_file = open(args.output, 'w', encoding='utf-8')

    try:
        if os.path.isdir(args.path):
            search_directory(args.path, args.keyword, args, out_file)
        else:
            grep_context(args.path, args.keyword, args.b, args.a, out_file, 
                         args.ignore_case, args.no_line_number, 
                         args.highlight, args.extended_regexp)
    finally:
        if out_file:
            out_file.close()