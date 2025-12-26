#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import math
import sys

# 確保環境中有 fontforge
try:
    import fontforge
except ImportError:
    print("Error: This script requires the 'fontforge' python module.")
    sys.exit(1)

def expand_stroke(args):
    # 1. 處理路徑與基本參數
    input_path = args.input
    output_path = args.output if args.output else input_path
    
    stroke_width = args.width
    expand_direction = args.expand_direction
    stroke_join_limit = 6  # 用於 light 模式

    print(f"--- Configuration ---")
    print(f"Input:    {input_path}")
    print(f"Output:   {output_path}")
    print(f"Width:    {stroke_width}")
    print(f"Mode:     {expand_direction}")
    print(f"---------------------")

    # 2. 開啟字體
    try:
        myfont = fontforge.open(input_path)
    except Exception as e:
        print(f"Failed to open font: {e}")
        return

    # 3. 更新字體元數據 (Metadata)
    # 定義需要從 args 同步到 myfont 的屬性清單
    font_attrs = ['comment', 'familyname', 'fontname', 'fullname', 'macstyle', 'weight']
    for attr in font_attrs:
        val = getattr(args, attr, None)
        if val is not None:
            setattr(myfont, attr, val)

    myfont.selection.all()
    
    # 4. 準備 Stroke 參數
    # 根據方向決定移除內部或外部輪廓
    is_bold = (expand_direction == "bold")
    stroke_params = {
        "stroke_type": "circular",
        "width": stroke_width,
        "cap": args.stroke_cap,
        "join": args.stroke_join,
        "angle": math.radians(45),
        "simplify": True,
        "removeoverlap": "contour"
    }

    if is_bold:
        stroke_params["removeinternal"] = True
    else:
        stroke_params["removeexternal"] = True
        stroke_params["joinlimit"] = stroke_join_limit

    # 5. 開始處理字元
    convert_count = 0
    total_selected = 0
    
    # 遍歷選中的字元
    for glyph in list(myfont.selection.byGlyphs):
        total_selected += 1
        
        # 過濾條件
        if glyph.unicode <= 0 or glyph.changed:
            continue
            
        # 執行擴展/描邊邏輯
        try:
            glyph.stroke(
                stroke_params["stroke_type"],
                stroke_params["width"],
                cap=stroke_params["cap"],
                join=stroke_params["join"],
                angle=stroke_params.get("angle", 0),
                removeinternal=stroke_params.get("removeinternal", False),
                removeexternal=stroke_params.get("removeexternal", False),
                simplify=stroke_params["simplify"],
                joinlimit=stroke_params.get("joinlimit", 0),
                removeoverlap=stroke_params["removeoverlap"]
            )
            convert_count += 1
        except Exception as e:
            print(f"Error processing {glyph.glyphname} (U+{glyph.unicode:04X}): {e}")

        if convert_count % 100 == 0 and convert_count > 0:
            print(f"Progress: Processed {convert_count} glyphs...")

    # 6. 儲存結果
    print(f"--- Finished ---")
    print(f"Total checked: {total_selected}")
    print(f"Converted:     {convert_count}")
    
    myfont.save(output_path)
    print(f"Result saved to: {output_path}")

def cli():
    parser = argparse.ArgumentParser(description="Expand font stroke using FontForge")
    parser.add_argument("--input", "-i", help="Input font file", required=True)
    parser.add_argument("--width", "-w", help="Stroke width", required=True, type=float)
    parser.add_argument("--expand_direction", choices=["bold", "light"], default="bold", help="Expand direction")
    parser.add_argument("--output", "-o", help="Output path (default: overwrite input)")
    
    # Font Metadata
    parser.add_argument("--comment", help="Font comment")
    parser.add_argument("--familyname", help="PostScript family name")
    parser.add_argument("--fontname", help="PostScript font name")
    parser.add_argument("--fullname", help="PostScript full name")
    parser.add_argument("--macstyle", type=int, help="Mac style bits")
    parser.add_argument("--weight", help="Font weight string")
    
    # Stroke Settings
    parser.add_argument("--stroke_cap", default='round', help="Line cap (round, butt, square)")
    parser.add_argument("--stroke_join", default='miter', help="Line join (miter, round, bevel)")
    
    args = parser.parse_args()
    expand_stroke(args)

if __name__ == "__main__":
    cli()