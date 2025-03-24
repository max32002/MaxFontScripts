import argparse
import os
from ChineseDictionary import ChineseDictionary

def find_characters_by_component(input_file, keyword, output_file):
    dictionary = ChineseDictionary()
    filtered_chars = []
    search_parts = []

    if input_file and os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            search_parts.extend(list(f.read().strip()))
    if keyword:
        search_parts.extend(list(keyword))

    if search_parts:  # 只有在 search_parts 有內容時才做比對
        for char in dictionary.data.keys():
            components = dictionary.component(char)
            if isinstance(components, dict):
                for part in search_parts:
                    if part in components.values() or part in components.keys():
                        filtered_chars.append(char)
                        break #找到一個部件就跳出，避免重複增加字
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("".join(filtered_chars))
        print(f"找到 {len(filtered_chars)} 個包含部件 {search_parts} 的字，已輸出到 {output_file}")
    else:
        print("沒有輸入部件，請輸入部件")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根據部件關鍵字篩選中文字")
    parser.add_argument("--input", help="輸入的文字檔 (可選)")
    parser.add_argument("--keyword", help="要查詢的部件關鍵字 (可選)")
    parser.add_argument("--output", default="output.txt", help="輸出的文字檔 (預設為 output.txt)")

    args = parser.parse_args()
    find_characters_by_component(args.input, args.keyword, args.output)