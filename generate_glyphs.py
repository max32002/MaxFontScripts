import argparse
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

def generate_glyph_images(keyword, font_path, font_size, canvas_size, output_dir, filename_rule, file_path=None, x_offset=0, y_offset=0, clear_output_dir=False):
    """
    使用指定參數生成字元圖像。
    """

    # 檢查字型檔案是否存在
    if not os.path.exists(font_path):
        print(f"錯誤：找不到字型檔案 {font_path}")
        return

    try:
        font1 = ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"錯誤：無法載入字型檔案 {font_path}")
        return

    if clear_output_dir and os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir)  # 刪除整個目錄
            print(f"已清除輸出目錄：{output_dir}")
        except Exception as e:
            print(f"警告：清除輸出目錄時發生錯誤：{e}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    characters = list(keyword)

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                characters.extend(list(file_content))
        except FileNotFoundError:
            print(f"警告：找不到檔案 {file_path}")
        except Exception as e:
            print(f"警告：讀取檔案時發生錯誤： {e}")

    for i, char in enumerate(characters):
        image = Image.new('RGB', (canvas_size, canvas_size), 'white')
        draw1 = ImageDraw.Draw(image)

        # 計算偏移量以使文字居中
        canvas_center = canvas_size // 2

        draw1.text((canvas_center + x_offset, canvas_center + y_offset), char, font=font1, fill='black', anchor='mm')

        if filename_rule == 'seq':
            filename = f'{i:04d}.png'
        elif filename_rule == 'char':
            filename = f'{char}.png'
        elif filename_rule == 'unicode_int':
            filename = f'{ord(char)}.png'
        elif filename_rule == 'unicode_hex':
            filename = f'{ord(char):x}.png'
        else:
            filename = f'{i:04d}.png' # 預設

        try:
            image.save(os.path.join(output_dir, filename))
            #print(f'已儲存 {filename}')
        except Exception as e:
            print(f"警告：儲存檔案 {filename} 時發生錯誤： {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成字元圖像。')
    parser.add_argument('--keyword', default="", help='要生成的字串。')
    parser.add_argument('--font', required=True, help='字型檔案的路徑。')
    parser.add_argument('--font_size', type=int, default=256, help='字型大小。')
    parser.add_argument('--canvas_size', type=int, default=256, help='圖布大小 (邊長)。')
    parser.add_argument('--output_dir', default='glyph_image', help='輸出目錄。')
    parser.add_argument('--filename_rule', type=str, default="unicode_int", choices=['seq', 'char', 'unicode_int', 'unicode_hex'], help="檔案名稱規則")
    parser.add_argument('--file', type=str, help='從文字檔案讀取字元。')
    parser.add_argument("--x_offset", type=int, default=0, help="字型 X 軸偏移量，預設為 0。")
    parser.add_argument("--y_offset", type=int, default=0, help="字型 Y 軸偏移量，預設為 0。")
    parser.add_argument("--clear", action="store_true", help="清除輸出目錄中的所有檔案。")

    args = parser.parse_args()

    generate_glyph_images(args.keyword, args.font, args.font_size, args.canvas_size, args.output_dir, args.filename_rule, args.file, args.x_offset, args.y_offset, args.clear)
    print(f'字元圖像已儲存至 {args.output_dir}')