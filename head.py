import argparse
from itertools import islice

def head_fast(file_path, n=10, output_path=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 取得前 n 行內容
            lines = [line.strip() for line in islice(f, n)]
            
            output_content = "\n".join(lines)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(output_content)
                print(f"結果已輸出至: {output_path}")
            else:
                for line in lines:
                    print(line)
                    
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="讀取檔案前幾行")
    parser.add_argument("file", help="目標檔案路徑")
    parser.add_argument("n", type=int, help="讀取的行數")
    parser.add_argument("-o", "--output", help="輸出到指定文字檔")

    args = parser.parse_args()
    
    head_fast(args.file, args.n, args.output)