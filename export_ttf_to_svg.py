#!/usr/bin/env python3
#encoding=utf-8

import os
import sys

def export_ttf_to_svg(ttf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    font = fontforge.open(ttf_path)

    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            #char_name = glyph.glyphname
            unicode_int = glyph.unicode

            # redirect for same case
            redirect_dict = {}
            redirect_dict = {19981: 63847, 20018: 63749, 20025: 63838, 20160: 63997, 20358: 63789, 20363: 63925, 20415: 63845, 20698: 63931, 20800: 20800, 20841: 63864, 21015: 63900, 21033: 63965, 21050: 63999, 21147: 63882, 21193: 21193, 21202: 63826, 21220: 21220, 21329: 21329, 21477: 63750, 21519: 63966, 21570: 63872, 21895: 63755, 22696: 22696, 22744: 63818, 23615: 63933, 24180: 63886, 24324: 63811, 24459: 63960, 25078: 63757, 25299: 64002, 26131: 63968, 26248: 63941, 26292: 64006, 26356: 63745, 26519: 63988, 27347: 63793, 27784: 63858, 27931: 63765, 27934: 64005, 28107: 63989, 28651: 63778, 28872: 63903, 29662: 63767, 29702: 63972, 30053: 63862, 30064: 63842, 30865: 30865, 30922: 63815, 34892: 64008, 35023: 63975, 35211: 64010, 35912: 63744, 36034: 63816, 36040: 63747, 36335: 63799, 36554: 63746, 36667: 64007, 37324: 63977, 37327: 63870, 38317: 63878, 38446: 63942, 38534: 38534, 39409: 63770, 39791: 63801, 40442: 63802}
            if unicode_int in redirect_dict:
                unicode_int = redirect_dict[unicode_int]

            svg_path = os.path.join(output_dir, f"{unicode_int}.svg")
            glyph.export(svg_path)
            print(f"Exported: {svg_path}")

    font.close()
    print("All glyphs exported to SVG.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python export_ttf_to_svg.py <ttf檔案路徑> <輸出資料夾>")
        sys.exit(1)

    ttf_file = sys.argv[1]
    output_folder = sys.argv[2]

    export_ttf_to_svg(ttf_file, output_folder)
