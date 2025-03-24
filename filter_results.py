import argparse

def filter_and_save_results(input_file, output_file, threshold=9.00):
    """
    開啟文字檔，取出差異百分比小於等於閾值的行，並將單引號之間的文字另存為新的文字檔。

    Args:
        input_file (str): 輸入文字檔的路徑。
        output_file (str): 輸出文字檔的路徑。
        threshold (float): 篩選的百分比閾值，預設為 9.00。
    """

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if "整體" in line:
                    try:
                        # 提取百分比數值
                        percentage = float(line.split("整體 ")[1].split("%")[0])
                        if percentage <= threshold:
                            # 提取單引號之間的文字
                            char = line.split("'")[1]
                            outfile.write(char + "\n")
                    except ValueError:
                        # 如果無法轉換為浮點數，則忽略該行
                        pass

        print(f"已成功篩選並將結果儲存至 {output_file}")

    except FileNotFoundError:
        print(f"錯誤：找不到輸入檔案 {input_file}")
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == "__main__":
    # 設定參數
    parser = argparse.ArgumentParser(description="篩選文字檔中的差異百分比結果，並輸出單引號之間的文字。")
    parser.add_argument("--input", required=True, help="輸入文字檔的路徑。")
    parser.add_argument("--output", default="filter_result.txt", help="輸出文字檔的路徑。")
    parser.add_argument("--threshold", type=float, default=9.00, help="篩選的百分比閾值，預設為 9.00。")
    args = parser.parse_args()

    # 執行篩選和儲存
    filter_and_save_results(args.input, args.output, args.threshold)
