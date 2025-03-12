import argparse
from ChineseDictionary import ChineseDictionary

def filter_characters(input_file, strokes_more, radical, radical_count, output_file):
    dictionary = ChineseDictionary()
    
    # 讀取輸入檔案
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    filtered_chars = []
    
    for char in content:
        strokes = dictionary.strokes_total(char)
        rad = dictionary.radical(char)
        rad_count = dictionary.radical_count(char)

        # 檢查筆畫數條件
        if strokes_more is not None and (strokes is None or strokes < strokes_more):
            continue

        # 檢查部首條件
        if radical is not None and rad != radical:
            continue

        # 檢查部首筆畫數條件（等於）
        if radical_count is not None and (rad_count is None or rad_count != radical_count):
            continue

        filtered_chars.append(char)

    # 輸出到指定檔案
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(filtered_chars))

    print(f"篩選完成！符合條件的字已輸出到 {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="篩選符合條件的中文字")
    parser.add_argument("--input", required=True, help="輸入的文字檔")
    parser.add_argument("--strokes_more", type=int, help="筆畫數門檻，篩選 >= 該數值的字")
    parser.add_argument("--radical", type=str, help="部首過濾，篩選部首為該值的字")
    parser.add_argument("--radical_count", type=int, help="部首筆畫數過濾，篩選 = 該數值的字")
    parser.add_argument("--output", required=True, help="輸出的文字檔")

    args = parser.parse_args()
    filter_characters(args.input, args.strokes_more, args.radical, args.radical_count, args.output)
