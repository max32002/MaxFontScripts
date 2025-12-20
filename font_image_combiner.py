#!/usr/bin/env python3
# encoding=utf-8
import argparse
import collections
import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from torch import nn
from torchvision import transforms
from tqdm import tqdm


def render_char(char, font, canvas_size, x_offset=0, y_offset=0):
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

def create_collage(char, image_dir, target_font, canvas_size,
                   target_x_offset, target_y_offset,
                   filtered_hashes, reverse, auto_fit=True):
    target_image = draw_character(
        char, target_font, canvas_size,
        target_x_offset, target_y_offset,
        auto_fit=auto_fit
    )

    if target_image is None:
        print(f"渲染字元失敗：{char}")
        return None

    if hash(target_image.tobytes()) in filtered_hashes:
        return None

    source_image_path = Path(image_dir) / f"{ord(char)}.png"
    if not source_image_path.exists():
        print(f"找不到來源圖像：{source_image_path}")
        return None

    source_image = Image.open(source_image_path)

    # 尺寸檢查與 resize
    w, h = source_image.size
    if w != canvas_size or h != canvas_size:
        source_image = source_image.resize(
            (canvas_size, canvas_size),
            resample=Image.LANCZOS
        )

    font_x_position = canvas_size if reverse else 0
    image_x_position = 0 if reverse else canvas_size

    example_image = Image.new(
        "RGB",
        (canvas_size * 2, canvas_size),
        (255, 255, 255)
    )

    example_image.paste(target_image, (font_x_position, 0))
    example_image.paste(source_image, (image_x_position, 0))

    image_binary = example_image.convert("1", dither=Image.NONE)

    return image_binary



def filter_recurring_hashes(charset, font, canvas_size, x_offset, y_offset):
    """過濾字型中重複的雜湊值。"""
    sample = np.random.choice(charset, min(2000, len(charset)), replace=False)
    hash_counts = collections.defaultdict(int)
    for char in sample:
        image = draw_character(char, font, canvas_size, x_offset, y_offset)
        hash_counts[hash(image.tobytes())] += 1
    return {hash_val for hash_val, count in hash_counts.items() if count > 2}


def process_images(image_dir, font_path, charset, char_size, canvas_size, target_x_offset, target_y_offset,
                   output_dir, filename_prefix="", filename_rule="seq", filter_hashes=True, reverse=False, auto_fit=True):
    """處理圖像並儲存範例。"""
    target_font = ImageFont.truetype(str(font_path), size=char_size)
    filtered_hashes = filter_recurring_hashes(charset, target_font, canvas_size, target_x_offset, target_y_offset) if filter_hashes else set()
    print(f"過濾雜湊值：{', '.join(map(str, filtered_hashes))}")

    count = 0
    for char in tqdm(charset, desc="處理字元"):
        image_binary = create_collage(char, image_dir, target_font, canvas_size, target_x_offset,
                                        target_y_offset, filtered_hashes, reverse, auto_fit=auto_fit)
        if image_binary is not None:
            filename = "%05d" % (count)
            if filename_rule=="unicode_int":
                filename = f"{ord(char)}"
            if filename_rule=="unicode_hex":
                filename = f"{ord(char):x}"
            target_filename = filename_prefix + filename + ".png"
            output_path = str(Path(output_dir) / f"{target_filename}")
            image_binary.save(output_path)
            count += 1

def main(args):
    """主函數。"""
    image_dir = Path(args.image_dir).resolve()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.image_dir is None or args.font_path is None:
        raise ValueError('必須提供 image_dir 和 font_path。')

    if args.charset:
        charset = list(open(args.charset, encoding='utf-8').readline().strip())
    else:
        charset = [chr(int(file.stem)) for file in image_dir.glob("*.png")]

    if args.shuffle:
        np.random.shuffle(charset)

    process_images(image_dir, args.font_path, charset, args.char_size, args.canvas_size, args.target_x_offset,
                    args.target_y_offset, output_dir, args.filename_prefix, args.filename_rule, args.filter_hashes, args.reverse, not args.disable_auto_fit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成字型圖像範例。")

    # 檔案路徑參數
    parser.add_argument("--image_dir", type=Path, required=True, help="圖像目錄路徑。")
    parser.add_argument("--font_path", type=Path, required=True, help="字型檔案路徑。")
    parser.add_argument("--output_dir", type=Path, default=Path("output_dir"), help="輸出目錄路徑。")
    parser.add_argument("--charset", type=str, help="字元集檔案路徑（一行一個字元）。")

    # 圖像處理參數
    parser.add_argument("--canvas_size", type=int, default=256, help="畫布大小。")
    parser.add_argument("--char_size", type=int, default=256, help="字元大小。")
    parser.add_argument("--target_x_offset", type=int, default=0, help="目標字型 X 軸偏移量。")
    parser.add_argument("--target_y_offset", type=int, default=0, help="目標字型 Y 軸偏移量。")
    parser.add_argument("--disable_auto_fit", action="store_true", help="停用圖像自動調整大小。")
    parser.add_argument("--reverse", action="store_true", help="反轉源圖像和目標字型圖像的位置。")

    # 其他參數
    parser.add_argument('--filename_rule', type=str, default="seq", choices=['seq', 'char', 'unicode_int', 'unicode_hex'])
    parser.add_argument("--filename_prefix", type=str, default="", help="範例標籤（用於檔案名稱前綴）。")
    parser.add_argument("--filter_hashes", action="store_true", help="過濾重複的雜湊值。")
    parser.add_argument("--shuffle", action="store_true", help="處理字元集之前先隨機排序。")

    args = parser.parse_args()
    # 參數驗證
    if not args.image_dir.is_dir():
        parser.error(f"源圖像目錄不存在：{args.image_dir}")
    if not args.font_path.is_file():
        parser.error(f"目標字型檔案不存在：{args.font_path}")
    if args.canvas_size <= 0:
        parser.error("畫布大小必須為正數。")
    if args.char_size <= 0:
        parser.error("字元大小必須為正數。")

    args = parser.parse_args()

    main(args)
    