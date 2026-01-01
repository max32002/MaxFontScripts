#!/usr/bin/env python3
# encoding=utf-8

import argparse

def process_sets(args):
    try:
        # 讀取完整檔案內容並轉為集合
        with open(args.input, encoding='utf-8') as f:
            input_set = set(f.read().strip())
        
        with open(args.remove, encoding='utf-8') as f:
            remove_set = set(f.read().strip())

        # 定義運算模式對應表
        operations = {
            "subtract": input_set - remove_set,
            "sub": input_set - remove_set,
            "-": input_set - remove_set,
            "union": input_set | remove_set,
            "add": input_set | remove_set,
            "+": input_set | remove_set,
            "intersect": input_set & remove_set,
            "int": input_set & remove_set,
            "&": input_set & remove_set
        }

        if args.mode not in operations:
            print(f"Error: Invalid mode '{args.mode}'.")
            return

        target_set = operations[args.mode]
        
        # 排序並格式化結果
        sorted_chars = sorted(target_set)
        formatted_result = ''.join(sorted_chars)

        # 輸出統計資訊
        print(f"length of input file: {len(input_set)}")
        print(f"length of remove file: {len(remove_set)}")
        print(f"final length of target file: {len(target_set)}")

        # 寫入檔案
        if formatted_result:
            with open(args.output, 'w', encoding='utf-8') as outfile:
                outfile.write(formatted_result)
        else:
            print("Warning: Target set is empty. No file was written.")

    except FileNotFoundError:
        print("Error: Input or remove file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cli():
    parser = argparse.ArgumentParser(description="process char sets")
    parser.add_argument("--input", "-i", help="input text file", required=True, type=str)
    parser.add_argument("--remove", "-r", help="string to process", required=True, type=str)
    parser.add_argument("--output", "-o", help="output text file", default="new.txt", type=str)
    parser.add_argument("--mode", "-m", help="mode of operation", default="subtract", 
                        choices=["subtract", "sub", "-", "union", "add", "+", "intersect", "int", "&"], type=str)

    args = parser.parse_args()
    process_sets(args)

if __name__ == "__main__":
    cli()