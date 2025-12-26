#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from pathlib import Path

# 檢查是否能導入 fontforge
try:
    import fontforge
except ImportError:
    print("錯誤: 找不到 fontforge 模組。請確保已安裝 fontforge 並使用其內建的 python 環境。")
    sys.exit(1)

def generate_font(args):
    input_path = Path(args.input)
    
    # 1. 處理輸出路徑
    if args.output:
        output_path = Path(args.output)
    else:
        # 如果沒指定輸出，則將 .sfdir 替換成 .ttf，或是直接加上 .ttf
        output_path = input_path.with_suffix('.ttf') if input_path.suffix == '.sfdir' else input_path.with_name(input_path.stem + "_converted.ttf")

    if not input_path.exists():
        print(f"錯誤: 找不到輸入檔案 '{input_path}'")
        return

    try:
        print(f"正在開啟字體: {input_path}")
        myfont = fontforge.open(str(input_path))

        # 2. 自動更新字體元數據 (Metadata)
        # 定義需要檢查並賦值的屬性清單
        attrs = ['comment', 'familyname', 'fontname', 'fullname', 'macstyle', 'weight']
        for attr in attrs:
            val = getattr(args, attr)
            if val is not None:
                setattr(myfont, attr, val)
                print(f"更新 {attr}: {val}")

        # 3. 執行匯出
        print(f"正在儲存字體: {output_path}")
        
        # 根據 namelist 決定產生參數
        gen_kwargs = {}
        if args.namelist:
            gen_kwargs['namelist'] = 'AGL For New Fonts'
            
        myfont.generate(str(output_path), **gen_kwargs)
        myfont.close()
        print("完成！")

    except Exception as e:
        print(f"處理過程中發生錯誤: {e}")

def cli():
    parser = argparse.ArgumentParser(description="使用 FontForge 轉換字體格式並修改元數據")
    
    # 輸入輸出
    parser.add_argument("--input", "-i", help="輸入字體路徑 (.sfdir, .ttf, .otf 等)", required=True)
    parser.add_argument("--output", "-o", help="輸出字體路徑 (.ttf)")
    
    # 字體元數據屬性
    parser.add_argument("--comment", help="字體註解")
    parser.add_argument("--familyname", help="PostScript 字族名稱 (Family Name)")
    parser.add_argument("--fontname", help="PostScript 字體名稱 (Font Name)")
    parser.add_argument("--fullname", help="完整字體名稱 (Full Name)")
    parser.add_argument("--macstyle", help="Mac 樣式 (例如: 1 代表粗體)", type=int)
    parser.add_argument("--weight", help="字體粗細字串 (Weight)")
    
    # 其他設定
    parser.add_argument("--namelist", help="指定名稱列表 (預設為空，若給予任何值則使用 'AGL For New Fonts')", default="")
    
    args = parser.parse_args()
    generate_font(args)

if __name__ == "__main__":
    cli()