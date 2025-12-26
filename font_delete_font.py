#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from pathlib import Path

# 確保環境中有 fontforge
try:
    import fontforge
except ImportError:
    print("Error: FontForge python module not found. Please run this with fontforge python.")
    sys.exit(1)

def get_glyph_unicode_set(font):
    """
    從字體中提取所有 Unicode 編碼（包含 altuni）
    """
    unicode_set = set()
    for glyph in font.glyphs():
        # 排除無編碼或寬度為 0 的字符
        if glyph.unicode <= 0 or glyph.width <= 0:
            continue
        
        unicode_set.add(glyph.unicode)
        
        # 處理變體編碼 (Alternative Unicodes)
        if glyph.altuni:
            for alt_entry in glyph.altuni:
                # alt_entry 通常是 (unicode, variation_selector, reserved)
                if isinstance(alt_entry, tuple) and alt_entry[0] > 0:
                    unicode_set.add(alt_entry[0])
    return unicode_set

def process_font(input_path, remove_path, output_path):
    """
    執行字體字符刪除的核心邏輯
    """
    input_p = Path(input_path)
    remove_p = Path(remove_path)
    
    # 判斷輸出路徑
    if not output_path:
        # 如果沒指定輸出，預設儲存為 .sfdir 專案檔
        output_p = input_p.with_suffix('.sfdir')
    else:
        output_p = Path(output_path)

    print(f"[*] Input:  {input_p}")
    print(f"[*] Target: {remove_p}")
    print(f"[*] Output: {output_p}")

    # 開啟字體
    try:
        main_font = fontforge.open(str(input_p))
        remove_font = fontforge.open(str(remove_p))
    except Exception as e:
        print(f"Error opening font: {e}")
        return

    # 獲取要刪除的 Unicode 集合
    targets = get_glyph_unicode_set(remove_font)
    print(f"[*] Found {len(targets)} glyphs to potentially remove.")

    # 效能優化點：使用 selection.select 批次選取，而非迴圈 clear
    # 我們只選取存在於 main_font 且在 targets 清單中的字符
    found_to_remove = []
    for uni in targets:
        if uni in main_font:
            found_to_remove.append(uni)

    if found_to_remove:
        # 使用 tuple 傳入 unicode 列表進行批次選取
        main_font.selection.select(('unicode',), *found_to_remove)
        main_font.clear()
        print(f"[*] Successfully cleared {len(found_to_remove)} glyphs.")
        
        # 根據副檔名決定產生方式
        ext = output_p.suffix.lower()
        if ext in ['.ttf', '.woff', '.woff2', '.otf']:
            print(f"[*] Generating font file: {output_p}")
            main_font.generate(str(output_p))
        else:
            print(f"[*] Saving font project: {output_p}")
            main_font.save(str(output_p))
    else:
        print("[!] No matching glyphs found. No changes made.")

    main_font.close()
    remove_font.close()

def cli():
    parser = argparse.ArgumentParser(description="從 A 字體中移除所有 B 字體含有的字符")
    parser.add_argument("--input", "-i", help="來源字體檔案 (TTF/WOFF/SFDIR)", required=True)
    parser.add_argument("--remove", "-r", help="參考字體檔案 (要從來源中刪除的字符集)", required=True)
    parser.add_argument("--output", "-o", help="輸出路徑 (未指定則儲存為 .sfdir)", default=None)
    
    args = parser.parse_args()

    # 檢查檔案是否存在
    if not Path(args.input).exists():
        print(f"Error: Input path not found: {args.input}")
        return
    if not Path(args.remove).exists():
        print(f"Error: Remove path not found: {args.remove}")
        return

    process_font(args.input, args.remove, args.output)

if __name__ == "__main__":
    cli()