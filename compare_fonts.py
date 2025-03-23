import argparse
import os
from PIL import Image, ImageDraw, ImageFont

def compare_fonts(font1_path, font2_path, text_file, output_file="compare_result.txt", font_size=64, font1_x_offset=0, font1_y_offset=0, font2_x_offset=0, font2_y_offset=0, save=False, reverse=False, output_dir="comparison_images"):
    """
    比較兩個字型在顯示文字上的差異百分比，並將結果輸出到文件中。

    Args:
        font1_path (str): 第一個字型檔案的路徑。
        font2_path (str): 第二個字型檔案的路徑。
        text_file (str): 包含要比較文字的文字檔案路徑。
        output_file (str): 輸出結果的檔案路徑，預設為 compare_result.txt。
        font_size (int): 字型大小，預設為 64。
        font1_x_offset (int): 第一個字型 X 軸偏移量，預設為 0。
        font1_y_offset (int): 第一個字型 Y 軸偏移量，預設為 0。
        font2_x_offset (int): 第二個字型 X 軸偏移量，預設為 0。
        font2_y_offset (int): 第二個字型 Y 軸偏移量，預設為 0。
        save (bool): 是否儲存左右對照圖，預設為 False。
        reverse (bool): 是否反轉左右對照圖的左右位置，預設為 False。
        output_dir (str): 對照圖的輸出目錄，預設為 comparison_images。

    Returns:
        float: 所有字元的平均差異百分比。
    """

    try:
        # 載入字型
        font1 = ImageFont.truetype(font1_path, size=font_size)
        font2 = ImageFont.truetype(font2_path, size=font_size)

        # 讀取文字檔案
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # 逐個字元比較
        total_diff_percentage = 0
        results = []  # 儲存結果的列表
        for char in text:
            # 建立兩個字型顯示相同字元的圖片
            image1 = Image.new('RGB', (100, 100), 'white')  # 調整圖片大小
            draw1 = ImageDraw.Draw(image1)
            draw1.text((50 + font1_x_offset, 50 + font1_y_offset), char, font=font1, fill='black', anchor='mm')

            image2 = Image.new('RGB', (100, 100), 'white')
            draw2 = ImageDraw.Draw(image2)
            draw2.text((50 + font2_x_offset, 50 + font2_y_offset), char, font=font2, fill='black', anchor='mm')

            # 計算像素差異
            diff_pixels = 0
            total_pixels = image1.width * image1.height
            for x in range(image1.width):
                for y in range(image1.height):
                    if image1.getpixel((x, y)) != image2.getpixel((x, y)):
                        diff_pixels += 1

            # 計算差異百分比
            diff_percentage = (diff_pixels / total_pixels) * 100
            total_diff_percentage += diff_percentage
            results.append(f"字元 '{char}' 的差異百分比：{diff_percentage:.2f}%")

            # 儲存左右對照圖
            if save:
                # 確保輸出目錄存在
                os.makedirs(output_dir, exist_ok=True)
                if reverse:
                    comparison_image = Image.new('RGB', (200, 100), 'white')
                    comparison_image.paste(image2, (0, 0))
                    comparison_image.paste(image1, (100, 0))
                else:
                    comparison_image = Image.new('RGB', (200, 100), 'white')
                    comparison_image.paste(image1, (0, 0))
                    comparison_image.paste(image2, (100, 0))
                comparison_image.save(os.path.join(output_dir, f"{char}_comparison.png"))

        # 計算平均差異百分比
        average_diff_percentage = total_diff_percentage / len(text)
        results.append(f"所有字元的平均差異百分比：{average_diff_percentage:.2f}%")

        # 將結果寫入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(result + "\n")

        return average_diff_percentage

    except FileNotFoundError:
        print("錯誤：找不到指定的字型檔案或文字檔案。")
        return None
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None

if __name__ == "__main__":
    # 設定參數
    parser = argparse.ArgumentParser(description="比較兩個字型在顯示文字上的差異百分比。")
    parser.add_argument("--font1", help="第一個字型檔案的路徑。")
    parser.add_argument("--font2", help="第二個字型檔案的路徑。")
    parser.add_argument("--file", help="包含要比較文字的文字檔案路徑。")
    parser.add_argument("--output_file", help="輸出結果的檔案路徑。", default="compare_result.txt")
    parser.add_argument("-s", "--size", type=int, default=64, help="字型大小，預設為 64。")
    parser.add_argument("--font1_x_offset", type=int, default=0, help="第一個字型 X 軸偏移量，預設為 0。")
    parser.add_argument("--font1_y_offset", type=int, default=0, help="第一個字型 Y 軸偏移量，預設為 0。")
    parser.add_argument("--font2_x_offset", type=int, default=0, help="第二個字型 X 軸偏移量，預設為 0。")
    parser.add_argument("--font2_y_offset", type=int, default=0, help="第二個字型 Y 軸偏移量，預設為 0。")
    parser.add_argument("--save", action="store_true", help="儲存左右對照圖。")
    parser.add_argument("--reverse", action="store_true", help="反轉左右對照圖的左右位置。")
    parser.add_argument("--output_dir", type=str, default="comparison_images", help="對照圖的輸出目錄，預設為 comparison_images。")
    args = parser.parse_args()

    average_diff = compare_fonts(args.font1, args.font2, args.file, args.output_file, args.size, args.font1_x_offset, args.font1_y_offset, args.font2_x_offset, args.font2_y_offset, args.save, args.reverse, args.output_dir)
    if average_diff is not None:
        print(f"所有字元的平均差異百分比：{average_diff:.2f}%")
