#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pathlib import Path

# 確保環境中有 fontforge
try:
    import fontforge
except ImportError:
    print("錯誤：找不到 fontforge 模組。請確保已安裝 fontforge 並在正確的環境中執行。")
    sys.exit(1)

def save_as(args):
    input_path = Path(args.input)
    
    # 1. 自動生成輸出路徑 (使用 pathlib 處理更安全)
    if args.output:
        out_path = Path(args.output)
    else:
        if input_path.suffix.lower() in ['.ttf', '.otf']:
            out_path = input_path.with_suffix('.sfdir')
        else:
            print(f"錯誤：無法從 '{input_path.name}' 自動生成輸出路徑。")
            return

    if not input_path.exists():
        print(f"錯誤：找不到輸入檔案 '{input_path}'")
        return

    print(f"正在開啟字型：{input_path}")
    try:
        myfont = fontforge.open(str(input_path))
    except Exception as e:
        print(f"開啟字型失敗：{e}")
        return

    # 2. 批次處理字型屬性 (減少重複的 if 判斷)
    font_attrs = [
        'comment', 'familyname', 'fontname', 
        'fullname', 'macstyle', 'weight'
    ]
    for attr in font_attrs:
        val = getattr(args, attr)
        if val is not None:
            setattr(myfont, attr, val)

    # 3. 字型合併邏輯
    if args.merge:
        print(f"正在合併字型：{args.merge}")
        # preserveCrossFontKerning=True
        myfont.mergeFonts(args.merge, True)

    # 4. 儲存與輸出
    print(f"正在儲存 sfdir：{out_path}")
    myfont.save(str(out_path))
    print("完成！ ^_^")

def cli():
    parser = argparse.ArgumentParser(description="使用 FontForge 進行字型轉換與處理")
    parser.add_argument("--input", "-i", help="輸入字型路徑", required=True)
    parser.add_argument("--output", "-o", help="輸出路徑 (預設轉換為 .sfdir)")
    parser.add_argument("--merge", "-m", help="要合併進來的字型檔案路徑")
    
    # 字型資訊相關參數
    group = parser.add_argument_group("字型資訊設定")
    group.add_argument("--comment", help="字型註解")
    group.add_argument("--familyname", help="PostScript Family Name")
    group.add_argument("--fontname", help="PostScript Font Name")
    group.add_argument("--fullname", help="Full Name")
    group.add_argument("--macstyle", type=int, help="Mac Style (例如：1 代表加粗)")
    group.add_argument("--weight", help="Weight 字串")

    args = parser.parse_args()
    save_as(args)

if __name__ == "__main__":
    cli()