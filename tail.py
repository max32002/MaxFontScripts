import os
import sys
import argparse

def tail_file(file_path, n=10, output_path=None):
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            buffer_size = 1024
            lines_found = 0
            data = []
            
            pos = file_size
            while pos > 0 and lines_found <= n:
                pos = max(0, pos - buffer_size)
                f.seek(pos)
                chunk = f.read(buffer_size)
                lines_found += chunk.count(b'\n')
                data.insert(0, chunk)
            
            content = b"".join(data).splitlines()
            last_lines = content[-n:]
            
            # 準備輸出的文字
            output_text = "\n".join(line.decode('utf-8') for line in last_lines)
            
            # 判斷是印在螢幕還是寫入檔案
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(output_text)
            else:
                print(output_text)
                
    except FileNotFoundError:
        print("找不到檔案")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="讀取檔案最後幾行")
    parser.add_argument("file", help="目標檔案路徑")
    parser.add_argument("lines", type=int, help="要讀取的行數")
    parser.add_argument("-o", "--output", help="輸出到指定的文字檔")
    
    args = parser.parse_args()
    
    tail_file(args.file, args.lines, args.output)