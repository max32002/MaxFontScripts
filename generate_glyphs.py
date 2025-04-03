import os
import shutil
import logging
import argparse
from PIL import Image, ImageDraw, ImageFont

import cv2  # OpenCV
import numpy as np
import freetype # For TTF font handling

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
    """根據規則生成檔案名稱。(與先前版本相同)"""
    if filename_rule == 'seq':
        return f'{seq_num:04d}.png'
    elif filename_rule == 'char':
        # 對於可能包含不適合做檔名的字元進行處理 (例如 / \ : * ? " < > |)
        safe_char = "".join(c for c in char if c.isalnum() or c in (' ', '.', '_')).rstrip()
        if not safe_char: # 如果字元本身就是特殊符號，給個替代名稱
             safe_char = f'char_{seq_num:04d}'
        return f'{safe_char}.png'
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

def draw_character_cv(char, face, font_size, canvas_size, x_offset, y_offset, background_color_bgr=(255, 255, 255)):
    """
    使用 FreeType 和 OpenCV 繪製單個字元圖像 (BGR)。
    字元將根據其在字型中的度量標準進行定位。
    (x_offset, y_offset) 用於調整字元原點 (基準線上的點) 相對於畫布上的參考點的位置。
    """
    if not face:
        logging.error("錯誤: 無效的 FreeType face 物件。")
        return None

    try:
        # 設定字型大小 (需要在讀取 face.size metrics 之前設定)
        face.set_pixel_sizes(0, font_size)

        # 載入字元 glyph 並渲染成灰度 bitmap
        # 使用 FT_LOAD_TARGET_NORMAL for anti-aliased grayscale
        face.load_char(char, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)

        # 獲取渲染後的 bitmap 資料
        bitmap = face.glyph.bitmap
        glyph_rows = bitmap.rows
        glyph_width = bitmap.width
        glyph_buffer = bitmap.buffer

        # 如果 glyph 為空 (例如空格或字型不支援)
        if glyph_rows == 0 or glyph_width == 0:
             # logging.info(f"字元 '{char}' 的 glyph 為空，返回空白畫布。")
             return np.full((canvas_size, canvas_size, 3), background_color_bgr, dtype=np.uint8)

        # 將 buffer 轉換為 NumPy array (灰度圖像)
        glyph_gray = np.array(glyph_buffer, dtype=np.uint8).reshape(glyph_rows, glyph_width)

        # --- 計算字元定位 ---
        # 1. 定義畫布上的參考基準線 Y 座標 (例如，設為 font_size 或接近頂部)
        #    使用 font_size 作為 y=0 時的基準線，更容易預測。
        baseline_ref_y = font_size # 當 y_offset=0 時，基準線在 y=font_size 處

        # 2. 計算目標 "畫筆位置" (字元原點) 在畫布上的座標
        pen_x = x_offset
        pen_y = baseline_ref_y + y_offset # 應用 y_offset 調整基準線

        # 3. 獲取字元相對於原點的度量標準
        bitmap_left = face.glyph.bitmap_left # 從原點到 bitmap 左邊緣的水平距離
        bitmap_top = face.glyph.bitmap_top   # 從原點(基準線)到 bitmap 頂部的垂直距離 (FreeType中通常向上為正)

        # 4. 計算 bitmap 左上角在畫布上的實際貼上座標 (paste_x, paste_y)
        paste_x = pen_x + bitmap_left
        # 因為畫布 Y 軸向下為正，而 bitmap_top 向上為正，所以用減法
        paste_y = pen_y - bitmap_top

        # --- 創建畫布並貼上 glyph ---
        # 創建 BGR 白色畫布
        canvas = np.full((canvas_size, canvas_size, 3), background_color_bgr, dtype=np.uint8)

        # --- (邊界裁剪邏輯 - 與之前版本相同) ---
        # 確定實際能貼上的區域 (避免超出邊界)
        x_start_canvas = max(paste_x, 0)
        y_start_canvas = max(paste_y, 0)
        x_end_canvas = min(paste_x + glyph_width, canvas_size)
        y_end_canvas = min(paste_y + glyph_rows, canvas_size)

        glyph_x_start = max(0, -paste_x)
        glyph_y_start = max(0, -paste_y)
        glyph_width_to_paste = x_end_canvas - x_start_canvas
        glyph_height_to_paste = y_end_canvas - y_start_canvas
        glyph_x_end = glyph_x_start + glyph_width_to_paste
        glyph_y_end = glyph_y_start + glyph_height_to_paste

        if glyph_width_to_paste <= 0 or glyph_height_to_paste <= 0:
             # logging.info(f"字元 '{char}' 計算出的貼上位置完全超出畫布範圍。")
             return canvas

        roi = canvas[y_start_canvas:y_end_canvas, x_start_canvas:x_end_canvas]
        glyph_part = glyph_gray[glyph_y_start:glyph_y_end, glyph_x_start:glyph_x_end]

        if roi.shape[:2] != glyph_part.shape[:2]:
             logging.warning(f"字元 '{char}' 的 ROI ({roi.shape[:2]}) 與 glyph part ({glyph_part.shape[:2]}) 尺寸不匹配。跳過貼上。")
             return canvas
        # --- (邊界裁剪邏輯結束) ---


        # --- (貼上邏輯 - 與之前版本相同) ---
        # 創建遮罩並貼上黑色字元
        mask = cv2.cvtColor(glyph_part, cv2.COLOR_GRAY2BGR)
        boolean_mask = mask[:,:,0] > 0 # Use grayscale value for mask

        char_black_bgr = np.zeros_like(roi)
        np.copyto(roi, char_black_bgr, where=boolean_mask[:,:,np.newaxis])
        # --- (貼上邏輯結束) ---

        return canvas

    except freetype.freetype.FT_Exception as e:
        logging.error(f"處理字元 '{char}' 時 FreeType 發生錯誤: {e}")
        return np.full((canvas_size, canvas_size, 3), background_color_bgr, dtype=np.uint8)
    except Exception as e:
        logging.error(f"處理字元 '{char}' 時發生未知錯誤: {e}")
        return np.full((canvas_size, canvas_size, 3), background_color_bgr, dtype=np.uint8)

def is_image_blank_cv(image_bgr, background_color_bgr=(255, 255, 255)):
    """檢查 OpenCV BGR 圖像是否完全為指定的背景色。"""
    if image_bgr is None:
        return True
    # 檢查是否所有像素都等於背景色
    return np.all(image_bgr == background_color_bgr)

def generate_glyph_images_cv(keyword, font_path, font_size, canvas_size, output_dir, filename_rule, file_path=None, x_offset=0, y_offset=0, clear_output_dir=False, threshold_value=128, disable_binary=False):
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
        filename = generate_filename(char, filename_rule, i)
        output_path = os.path.join(output_dir, filename)

        # 創建 BGR 圖像 (包含文字)
        image_bgr = draw_character_cv(char, face, font_size, canvas_size, x_offset, y_offset, background_bgr)

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
    parser.add_argument("--threshold", type=int, default=128, help="二極化的閾值 (0-255) (預設: 128)。")

    args = parser.parse_args()

    # 檢查 canvas_size 是否足夠大
    if args.canvas_size < args.font_size:
         logging.warning(f"警告: 畫布大小 ({args.canvas_size}) 小於字體大小 ({args.font_size})，字元可能無法完整顯示。建議增加 canvas_size。")

    # 執行生成函數
    '''
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
    '''
    generate_glyph_images_cv(
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
        threshold_value=args.threshold,
        disable_binary=args.disable_binary
    )

    print(f'字元圖像已儲存至 {args.output_dir}')