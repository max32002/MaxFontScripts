import os
import collections
import argparse

def output_text(text, file_handle=None):
    print(text)
    if file_handle:
        file_handle.write(text + "\n")

def grep_context(file_path, keyword, before=2, after=2, out_f=None, ignore_case=False):
    before_history = collections.deque(maxlen=before)
    after_count = 0
    found_any = False
    
    # 預先處理搜尋關鍵字
    search_keyword = keyword.lower() if ignore_case else keyword

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                
                # 根據參數決定是否忽略大小寫進行比對
                match_line = clean_line.lower() if ignore_case else clean_line
                
                if search_keyword in match_line:
                    if not found_any:
                        output_text(f"\n>>> 檔案: {file_path}", out_f)
                        found_any = True
                    
                    while before_history:
                        h_line = before_history.popleft()
                        output_text(f"{line_num - len(before_history) - 1}: {h_line}", out_f)
                    
                    output_text(f"{line_num}* {clean_line}", out_f)
                    after_count = after
                elif after_count > 0:
                    output_text(f"{line_num}: {clean_line}", out_f)
                    after_count -= 1
                else:
                    before_history.append(clean_line)
    except Exception:
        pass

def search_directory(root_path, keyword, before, after, extension, out_f=None, ignore_case=False):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                grep_context(full_path, keyword, before, after, out_f, ignore_case)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="要搜尋的關鍵字")
    parser.add_argument("path", help="檔案路徑或資料夾路徑")
    parser.add_argument("-b", type=int, default=2, help="顯示前幾行")
    parser.add_argument("-a", type=int, default=2, help="顯示後幾行")
    parser.add_argument("-ext", default=".log", help="指定副檔名 (預設 .log)")
    parser.add_argument("-o", "--output", help="將結果輸出到指定檔案")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小寫")
    
    args = parser.parse_args()

    out_file = None
    if args.output:
        out_file = open(args.output, 'w', encoding='utf-8')

    try:
        if os.path.isdir(args.path):
            search_directory(args.path, args.keyword, args.b, args.a, args.ext, out_file, args.ignore_case)
        else:
            grep_context(args.path, args.keyword, args.b, args.a, out_file, args.ignore_case)
    finally:
        if out_file:
            out_file.close()