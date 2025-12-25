import argparse
import os
import shutil

import cv2
import numpy as np
import freetype
from PIL import Image, ImageDraw, ImageFont

import logging

class SimpleColorFormatter(logging.Formatter):
    # 定義顏色碼
    COLORS = {
        'INFO': "\x1b[32mINFO\x1b[0m",
        'WARNING': "\x1b[33mWARNING\x1b[0m",
        'ERROR': "\x1b[31mERROR\x1b[0m",
        'DEBUG': "\x1b[36mDEBUG\x1b[0m",
    }

    def format(self, record):
        level_name = self.COLORS.get(record.levelname, record.levelname)
        return f"{level_name}: {record.getMessage()}"

# 套用設定
handler = logging.StreamHandler()
handler.setFormatter(SimpleColorFormatter())
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)


# 設定日誌記錄
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(levelname).1s: %(message)s')

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

def generate_filename(char, filename_rule, file_format, seq_num):
    """根據規則生成檔案名稱。(與先前版本相同)"""
    if filename_rule == 'seq':
        return f'{seq_num:04d}.{file_format}'
    elif filename_rule == 'char':
        # 對於可能包含不適合做檔名的字元進行處理 (例如 / \ : * ? " < > |)
        safe_char = "".join(c for c in char if c.isalnum() or c in (' ', '.', '_')).rstrip()
        if not safe_char: # 如果字元本身就是特殊符號，給個替代名稱
             safe_char = f'char_{seq_num:04d}'
        return f'{safe_char}.{file_format}'
    elif filename_rule == 'unicode_int':
        return f'{ord(char)}.{file_format}'
    elif filename_rule == 'unicode_hex':
        return f'{ord(char):x}.{file_format}'
    else:
        return f'{seq_num:04d}.{file_format}' # 預設

def render_char(char, font, canvas_size, x_offset=0, y_offset=0): 
    mask = font.getmask(char) 
    if not mask.getbbox(): 
        #print(f"字體不支援這個字: {char}") 
        return None

    img = Image.new("L", (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), char,  fill=0, font=font )
    return img

def draw_character(char, font, canvas_size, x_offset=0, y_offset=0, auto_fit=True):
    """渲染單個字元到圖像。"""
    img = None
    if auto_fit:
        img = Image.new("L", (canvas_size * 2, canvas_size * 2), 0)
        draw = ImageDraw.Draw(img)
        draw.text((x_offset, y_offset), char, 255, font=font)

        bbox = img.getbbox()
        if bbox is None:
            print(f"警告：字型 '{font.path}' 中缺少字元 '{char}' 的 glyph。")
            return None
        l, u, r, d = bbox
        l = max(0, l - 5)
        u = max(0, u - 5)
        r = min(canvas_size * 2 - 1, r + 5)
        d = min(canvas_size * 2 - 1, d + 5)
        if l >= r or u >= d:
            print(f"警告：字型 '{font.path}' 中缺少字元 '{char}' 的 glyph。")
            return None
        img = np.array(img)
        img = img[u:d, l:r]
        img = 255 - img
        img = Image.fromarray(img)
        # img.show()
        width, height = img.size
        # Convert PIL.Image to FloatTensor, scale from 0 to 1, 0 = black, 1 = white
        try:
            img = transforms.ToTensor()(img)
        except Exception as e:
            print(f"Error ToTensor: {e}")
            return None
        img = img.unsqueeze(0)  # 加轴
        pad_len = int(abs(width - height) / 2)  # 预填充区域的大小
        # 需要填充区域，如果宽大于高则上下填充，否则左右填充
        if width > height:
            fill_area = (0, 0, pad_len, pad_len)
        else:
            fill_area = (pad_len, pad_len, 0, 0)
        # 填充像素常值
        fill_value = 1
        img = nn.ConstantPad2d(fill_area, fill_value)(img)
        img = img.squeeze(0)
        img = transforms.ToPILImage()(img)
        img = img.resize((canvas_size, canvas_size), Image.BILINEAR)
    else:
        img = render_char(char, font, canvas_size, x_offset, y_offset)
    return img

def is_image_blank(image):
    """檢查圖像是否完全空白。"""
    if not image:
        return True  # 如果圖像為 None，則視為空白

    extrema = image.getextrema()
    if extrema == ((255, 255), (255, 255), (255, 255)):
        return True  # 如果所有像素都是白色，則圖像為空白
    else:
        return False

def generate_glyph_images(keyword, font_path, font_size, canvas_size, output_dir, filename_rule, file_format="png", file_path=None, x_offset=0, y_offset=0, clear_output_dir=False, threshold_value=128, auto_fit=True, disable_binary=False):
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
        filename = generate_filename(char, filename_rule, file_format, i)
        output_path = os.path.join(output_dir, filename)

        # PIL
        image_bgr = draw_character(char, font, canvas_size, x_offset, y_offset, auto_fit=auto_fit)

        if image_bgr and not is_image_blank(image_bgr):
            try:
                image_binary = image_bgr
                # 進行二極化轉換
                # TODO: 判斷 threshold_value
                if not disable_binary:
                    image_binary = image_binary.convert("1", dither=Image.NONE)

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

def load_font_freetype(font_path):
    """載入字型檔案 using freetype-py."""
    face = None
    if not os.path.exists(font_path):
        logging.error(f"錯誤：找不到字型檔案 {font_path}")
        return None
    try:
        face = freetype.Face(font_path)
        logging.info(f"成功載入字型: {font_path}")
    except freetype.freetype.FT_Exception as e:
        logging.error(f"錯誤：無法載入字型檔案 {font_path} - {e}")
        return None
    return face

def draw_character_cv(char, face, font_size, canvas_size, x_offset, y_offset):
    if not face:
        logging.error("錯誤: 無效的 FreeType face 物件。")
        return None

        face.set_pixel_sizes(0, font_size)
        face.load_char(char, freetype.FT_LOAD_RENDER)

        glyph = face.glyph
        bitmap = glyph.bitmap

        canvas = np.full((canvas_size, canvas_size), 255, dtype=np.uint8)

        top = y_offset + face.size.ascender // 64 - glyph.bitmap_top
        left = x_offset + glyph.bitmap_left

        h, w = bitmap.rows, bitmap.width
        buffer = np.array(bitmap.buffer, dtype=np.uint8).reshape(h, w)

        if h > 0 and w > 0:
            canvas[top:top+h, left:left+w] = 255 - buffer        

        return canvas

def is_image_blank_cv(image_bgr, background_color_bgr=(255, 255, 255)):
    """檢查 OpenCV BGR 圖像是否完全為指定的背景色。"""
    if image_bgr is None:
        return True
    # 檢查是否所有像素都等於背景色
    return np.all(image_bgr == background_color_bgr)

def generate_glyph_images_cv(keyword, font_path, font_size, canvas_size, output_dir, filename_rule, file_format, file_path=None, x_offset=0, y_offset=0, clear_output_dir=False, threshold_value=128, disable_binary=False):
    """使用 OpenCV 和 FreeType 生成字元圖像，並進行二極化處理後儲存。"""
    face = load_font_freetype(font_path)
    if face is None:
        return

    # 檢查是否需要清除輸出目錄
    if clear_output_dir:
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
                logging.info(f"已清除輸出目錄：{output_dir}")
            except Exception as e:
                logging.warning(f"警告：清除輸出目錄時發生錯誤：{e}")

    # 確保輸出目錄存在
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"已建立輸出目錄: {output_dir}")
        except OSError as e:
            logging.error(f"錯誤：無法建立輸出目錄 {output_dir} - {e}")
            return

    characters = list(keyword)

    # 從檔案讀取額外字元
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                characters.extend(list("".join(file_content.split())))
        except FileNotFoundError:
            logging.warning(f"警告：找不到檔案 {file_path}")
        except Exception as e:
            logging.warning(f"警告：讀取檔案時發生錯誤： {e}")

    # 去重並保持順序
    unique_characters = []
    seen = set()
    for char in characters:
        if char not in seen:
            unique_characters.append(char)
            seen.add(char)

    if not unique_characters:
        print("沒有有效的字元需要處理。")
        return

    print(f"準備使用 OpenCV 和 FreeType 生成 {len(unique_characters)} 個字元的圖像...")

    # 生成字元圖像
    saved_count = 0
    skipped_count = 0
    background_bgr = (255, 255, 255) # OpenCV White background (BGR)

    for i, char in enumerate(unique_characters):
        filename = generate_filename(char, filename_rule, file_format, i)
        output_path = os.path.join(output_dir, filename)

        # 創建 BGR 圖像 (包含文字)
        image_bgr = draw_character_cv(char, face, font_size, canvas_size, x_offset, y_offset)

        # 檢查圖像是否有效且非空白
        if image_bgr is not None and not is_image_blank_cv(image_bgr, background_bgr):
            try:
                # --- 二極化處理 ---
                # 1. 轉換為灰度圖
                gray_img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

                # 2. 應用二進制閾值
                #    像素值 > threshold_value 變成 255 (白)
                #    像素值 <= threshold_value 變成 0 (黑)
                #    我們希望文字是黑(0)，背景是白(255)，所以使用 THRESH_BINARY_INV
                binary_img = gray_img
                if not disable_binary:
                    _retval, binary_img = cv2.threshold(gray_img, threshold_value, 255, cv2.THRESH_BINARY)

                # --- 儲存圖像 ---
                # 使用 cv2.imwrite 儲存二極化後的圖像
                success = cv2.imwrite(output_path, binary_img)
                if success:
                    saved_count += 1
                    # logging.info(f'已儲存 {filename}')
                else:
                    logging.warning(f"警告：無法儲存檔案 {filename} (字元 '{char}')。cv2.imwrite 返回 False。")
                    skipped_count += 1

            except Exception as e:
                logging.warning(f"警告：處理或儲存檔案 {filename} (字元 '{char}') 時發生錯誤： {e}")
                skipped_count += 1
        else:
            # 跳過空白或無效圖像
            if char.isspace():
                 logging.info(f"提示：跳過空白字元 '{char}' (Unicode: {ord(char)}) 的圖像生成。")
            else:
                 logging.info(f"提示：跳過字元 '{char}' (Unicode: {ord(char)}) 的圖像生成，可能因為字型缺失、渲染錯誤或結果為空白。")
            skipped_count += 1

    print(f"圖像生成完成。成功儲存 {saved_count} 個圖像，跳過 {skipped_count} 個圖像。")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成字元圖像。')
    parser.add_argument("--clear", action="store_true", help="清除輸出目錄中的所有檔案。")
    parser.add_argument("--disable_binary", action="store_true", help="停用二極化")
    parser.add_argument("--threshold", type=int, default=128, help="二極化的閾值 (0-255) (預設: 128)。")
    parser.add_argument("--x_offset", type=int, default=0, help="字型 X 軸偏移量，預設為 0。")
    parser.add_argument("--y_offset", type=int, default=0, help="字型 Y 軸偏移量，預設為 0。")
    parser.add_argument("-f", "--format", default="png", help="目標檔案格式 (例如: pbm, png, jpg)")
    parser.add_argument('--canvas_size', type=int, default=256, help='圖布大小 (邊長)。')
    parser.add_argument('--disable_auto_fit', action='store_true', help='disable image auto fit')
    parser.add_argument('--file', type=str, help='從文字檔案讀取字元。')
    parser.add_argument('--filename_rule', type=str, default="unicode_int", choices=['seq', 'char', 'unicode_int', 'unicode_hex'], help="檔案名稱規則")
    parser.add_argument('--font', required=True, help='字型檔案的路徑。')
    parser.add_argument('--font_size', type=int, default=256, help='字型大小。')
    parser.add_argument('--keyword', default="", help='要生成的字串。')
    parser.add_argument('--output_dir', default='glyph_image', help='輸出目錄。')

    args = parser.parse_args()

    # 檢查 canvas_size 是否足夠大
    if args.canvas_size < args.font_size:
         logging.warning(f"警告: 畫布大小 ({args.canvas_size}) 小於字體大小 ({args.font_size})，字元可能無法完整顯示。建議增加 canvas_size。")

    # 執行生成函數
    '''
    generate_glyph_images_cv(
        keyword=args.keyword,
        font_path=args.font,
        font_size=args.font_size,
        canvas_size=args.canvas_size,
        output_dir=args.output_dir,
        filename_rule=args.filename_rule,
        file_format=args.format,
        file_path=args.file,
        x_offset=args.x_offset,
        y_offset=args.y_offset,
        clear_output_dir=args.clear,
        threshold_value=args.threshold,
        disable_binary=args.disable_binary
    )
    '''

    auto_fit = True
    if args.disable_auto_fit:
        auto_fit = False

    generate_glyph_images(
        keyword=args.keyword,
        font_path=args.font, 
        font_size=args.font_size,
        canvas_size=args.canvas_size,
        output_dir=args.output_dir,
        filename_rule=args.filename_rule,
        file_format=args.format,
        file_path=args.file,
        x_offset=args.x_offset,
        y_offset=args.y_offset,
        clear_output_dir=args.clear,
        threshold_value=args.threshold,
        auto_fit=auto_fit,
        disable_binary=args.disable_binary
    )

    print(f'字元圖像已儲存至 {args.output_dir}')