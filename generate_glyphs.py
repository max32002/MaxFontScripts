import os
import shutil
import logging
import argparse
from PIL import Image, ImageDraw, ImageFont

# 設定日誌記錄
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_font(font_path, font_size):
    """載入字型檔案。"""
    font = None
    if not os.path.exists(font_path):
        logging.error(f"錯誤：找不到字型檔案 {font_path}")
        return None

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        logging.error(f"錯誤：無法載入字型檔案 {font_path}")
        return None
    return font

def generate_filename(char, filename_rule, seq_num):
    """根據規則生成檔案名稱。"""
    if filename_rule == 'seq':
        return f'{seq_num:04d}.png'
    elif filename_rule == 'char':
        return f'{char}.png'
    elif filename_rule == 'unicode_int':
        return f'{ord(char)}.png'
    elif filename_rule == 'unicode_hex':
        return f'{ord(char):x}.png'
    else:
        return f'{seq_num:04d}.png' # 預設

def draw_character(char, font, canvas_size, x_offset, y_offset, background_color = 'white'):
    """繪製單個字元圖像。"""
    image = Image.new('RGB', (canvas_size, canvas_size), background_color)
    draw = ImageDraw.Draw(image)
    draw.text((0 + x_offset, 0 + y_offset), char, (0, 0, 0), font=font)

    bbox = image.getbbox()
    if bbox is None:
        print(f"警告：字型 '{font.path}' 中缺少字元 '{char}' 的 glyph。")
        return None  # 直接返回 None，不儲存圖像
    else:
        #print(f"輸出：字元 '{char}' 的 glyph。")
        return image

def is_image_blank(image):
    """檢查圖像是否完全空白。"""
    if not image:
        return True  # 如果圖像為 None，則視為空白

    extrema = image.getextrema()
    if extrema == ((255, 255), (255, 255), (255, 255)):
        return True  # 如果所有像素都是白色，則圖像為空白
    else:
        return False

def generate_glyph_images(keyword, font_path, font_size, canvas_size, output_dir, filename_rule, file_path=None, x_offset=0, y_offset=0, clear_output_dir=False, disable_binary=False):
    """使用指定參數生成字元圖像。"""
    font = load_font(font_path, font_size)
    if font is None:
        return

    # 檢查是否需要清除輸出目錄
    if clear_output_dir:
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)  # 刪除整個目錄
                logging.info(f"已清除輸出目錄：{output_dir}")
            except Exception as e:
                logging.warning(f"警告：清除輸出目錄時發生錯誤：{e}")

    # 確保輸出目錄存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    characters = list(keyword)

    # 從檔案讀取額外字元
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                characters.extend(list(file_content))
        except FileNotFoundError:
            logging.warning(f"警告：找不到檔案 {file_path}")
        except Exception as e:
            logging.warning(f"警告：讀取檔案時發生錯誤： {e}")

    # 去重並保持順序 (如果需要)
    unique_characters = []
    seen = set()
    for char in characters:
        if char not in seen:
            unique_characters.append(char)
            seen.add(char)

    if not unique_characters:
        print("沒有有效的字元需要處理。")
        return

    print(f"準備生成 {len(unique_characters)} 個字元的圖像...")

    # 生成字元圖像
    saved_count = 0
    skipped_count = 0
    for i, char in enumerate(unique_characters):
        filename = generate_filename(char, filename_rule, i)
        output_path = os.path.join(output_dir, filename)

        image_rgb = draw_character(char, font, canvas_size, x_offset, y_offset, background_color='white')

        if image_rgb and not is_image_blank(image_rgb):
            try:
                image_binary = image_rgb
                # 進行二極化轉換
                if not disable_binary:
                    image_binary = image_rgb.convert('1')

                # 儲存二極化後的圖像
                image_binary.save(output_path)
                saved_count += 1
                # logging.info(f'已儲存 {filename}')
            except Exception as e:
                logging.warning(f"警告：處理或儲存檔案 {filename} (字元 '{char}') 時發生錯誤： {e}")
                skipped_count += 1
        else:
            # 如果 draw_character 返回 None 或空白圖像，則跳過儲存
            if char.isspace(): # 對於空白字符給出更明確的提示
                 logging.info(f"提示：跳過空白字元 '{char}' (Unicode: {ord(char)}) 的圖像生成。")
            else:
                 logging.info(f"提示：跳過字元 '{char}' (Unicode: {ord(char)}) 的圖像生成，可能因為字型缺失或繪製結果為空白。")
            skipped_count += 1

    print(f"圖像生成完成。成功儲存 {saved_count} 個圖像，跳過 {skipped_count} 個圖像。")

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
    parser.add_argument("--disable_binary", action="store_true", help="停用二極化")

    args = parser.parse_args()

    # 執行生成函數
    generate_glyph_images(
        keyword=args.keyword,
        font_path=args.font,
        font_size=args.font_size,
        canvas_size=args.canvas_size,
        output_dir=args.output_dir,
        filename_rule=args.filename_rule,
        file_path=args.file,
        x_offset=args.x_offset,
        y_offset=args.y_offset,
        clear_output_dir=args.clear,
        disable_binary=args.disable_binary
    )
    print(f'字元圖像已儲存至 {args.output_dir}')