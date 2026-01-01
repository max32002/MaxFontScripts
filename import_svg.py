#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fontforge
import os
import argparse
import re
from pathlib import Path

def get_svg_width_logic(svg_path, default_width=1000):
    """
    從第一個 SVG 檔案中解析寬度：
    1. 優先找 width 屬性。
    2. 若無，解析 viewBox="x y w h" 中的 w。
    """
    svg_dir = Path(svg_path)
    first_svg = next(svg_dir.glob("*.svg"), None)
    
    if not first_svg:
        print(f"警告：找不到 SVG 檔案，使用預設寬度 {default_width}")
        return default_width

    try:
        with open(first_svg, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 1. 嘗試抓取 width 屬性
            width_match = re.search(r'width="([\d\.]+)([a-z]*)"', content)
            if width_match:
                val = float(width_match.group(1))
                print(f"偵測到 width 屬性: {val} (檔案: {first_svg.name})")
                return int(val)

            # 2. 嘗試解析 viewBox (格式：viewBox="0 0 384 384" 或 "0,0,384,384")
            # 抓取雙引號內的內容
            viewbox_match = re.search(r'viewBox="([^"]+)"', content)
            if viewbox_match:
                vb_values = re.split(r'[,\s]+', viewbox_match.group(1).strip())
                if len(vb_values) >= 4:
                    # viewBox 的第三個參數是 width
                    val = float(vb_values[2])
                    print(f"偵測到 viewBox 寬度: {val} (檔案: {first_svg.name})")
                    return int(val)
                    
    except Exception as e:
        print(f"解析 SVG 標籤時發生錯誤: {e}")
    
    print(f"無法從檔案獲取規格，回退至預設值: {default_width}")
    return default_width

def import_svg_to_glyphs(myfont, svg_path, filename_rule, scale, simplify, detected_width):
    import_char_list = set()
    fail_char_list = set()
    
    svg_dir = Path(svg_path)
    svg_files = list(svg_dir.glob("*.svg"))
    total_files = len(svg_files)

    for idx, svg_file in enumerate(svg_files, 1):
        filename_stem = svg_file.stem
        
        # 轉換檔名為 Unicode
        try:
            if filename_rule == 'unicode_int':
                unicode_int = int(filename_stem)
            elif filename_rule == 'unicode_hex':
                unicode_int = int(filename_stem, 16)
            else:
                unicode_int = ord(filename_stem)
        except ValueError:
            fail_char_list.add(svg_file.name)
            continue

        try:
            # 快速檢查 Unicode 索引
            if unicode_int in myfont:
                glyph = myfont[unicode_int]
                previous_width = glyph.width
                glyph.clear()
                glyph.importOutlines(str(svg_file), scale=scale, simplify=simplify)
                glyph.width = previous_width 
            else:
                glyph = myfont.createChar(unicode_int)
                glyph.importOutlines(str(svg_file), scale=scale, simplify=simplify)
                glyph.width = detected_width 
            
            import_char_list.add(glyph.originalgid)
        except Exception as e:
            fail_char_list.add(unicode_int)

        if idx % 500 == 0:
            print(f"處理進度: {idx}/{total_files}")

    print(f"匯入完成。成功: {len(import_char_list)}, 失敗: {len(fail_char_list)}")
    return import_char_list

def import_main(args):
    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else None
    
    if not out_path:
        out_path = Path(f"{in_path.stem}.sfdir") if in_path.suffix == ".ttf" else in_path

    if not in_path.exists():
        print("錯誤：輸入檔案不存在。")
        return

    # 自動偵測寬度邏輯
    detected_width = get_svg_width_logic(args.svg_path)

    myfont = fontforge.open(str(in_path))

    imported = import_svg_to_glyphs(
        myfont, args.svg_path, args.filename_rule, 
        args.enable_scale, not args.disable_simplify, detected_width
    )

    if imported:
        # 批次更新字型元數據
        font_attrs = ['comment', 'familyname', 'fontname', 'fullname', 'weight']
        for attr in font_attrs:
            val = getattr(args, attr)
            if val is not None: setattr(myfont, attr, val)
        if args.macstyle is not None: myfont.macstyle = args.macstyle

        # 儲存邏輯
        if out_path.suffix.lower() in {'.ttf', '.woff', '.woff2', '.otf'}:
            myfont.generate(str(out_path))
        else:
            myfont.save(str(out_path))
        print(f"完成！字型已儲存至: {out_path}")
    else:
        print("未執行任何變更。")

def main():
    parser = argparse.ArgumentParser(description="進階 SVG 寬度偵測與字型匯入工具")
    parser.add_argument("--input", "-i", required=True, help="輸入字型 (.ttf/.sfdir)")
    parser.add_argument("--output", "-o", help="輸出路徑")
    parser.add_argument("--svg_path", "-s", default=".", help="SVG 資料夾")
    parser.add_argument("--filename_rule", "-f", choices=['char', 'unicode_hex', 'unicode_int'], 
                        default="unicode_int", help="檔名解析格式")
    parser.add_argument('--enable_scale', action='store_true', help='縮放至 Ascender')
    parser.add_argument('--disable_simplify', action='store_true', help='停用路徑簡化')
    
    # 字型資訊設定
    for attr in ['comment', 'familyname', 'fontname', 'fullname', 'weight']:
        parser.add_argument(f"--{attr}", type=str)
    parser.add_argument("--macstyle", type=int)

    args = parser.parse_args()
    
    if Path(args.svg_path).exists():
        import_main(args)
    else:
        print(f"錯誤：找不到路徑 {args.svg_path}")

if __name__ == "__main__":
    main()