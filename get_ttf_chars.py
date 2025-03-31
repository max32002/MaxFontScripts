#!/usr/bin/env python3
# encoding=utf-8

import argparse
import platform
import os
import logging
from pathlib import Path
from typing import Set, List

try:
    import fontforge
except ImportError:
    fontforge = None

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff', '.svg'}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_image_file(filename: str) -> bool:
    """檢查文件是否為圖像文件。 """
    return Path(filename).suffix.lower() in IMG_EXTENSIONS

def output_to_file(myfile, myfont_set: Set[int]) -> None:
    """將字符集輸出到文件。 """
    full_text: List[str] = [chr(item) for item in sorted(myfont_set) if 0 <= item < 0x110000]
    myfile.write(''.join(full_text))

def save_set_to_file(sorted_set: Set[int], filename_output: str) -> None:
    """將排序後的字符集保存到文件。 """
    encoding = 'UTF-8' if platform.system() == 'Windows' else None
    with open(filename_output, 'w', encoding=encoding) as outfile:
        output_to_file(outfile, sorted_set)

def process_font_file(source_path: str, source_unicode_set: Set[int]) -> None:
    """處理字體文件。 """
    if fontforge is None:
        logging.error("fontforge module is not installed.")
        return

    if not os.path.exists(source_path):
        logging.error(f"File not found: {source_path}")
        return

    try:
        if source_path.endswith((".ttf", ".otf", ".woff", ".woff2")):
            myfont = fontforge.open(source_path)
            myfont.selection.all()
            all_glyph_list = list(myfont.selection.byGlyphs)
            source_unicode_set.update(glyph.unicode for glyph in all_glyph_list if 0 <= glyph.unicode < 0x110000)
        elif source_path.endswith(".sfdir"):
            import LibGlyph
            source_unicode_set.update(LibGlyph.load_files_to_set_dict(source_path, 2)[0])
    except Exception as e:
        logging.error(f"Error processing font file: {source_path}, error: {e}")

def process_image_folder(source_path: str, source_unicode_set: Set[int]) -> None:
    """處理圖像文件夾。 """
    source_path_obj = Path(source_path)
    if not source_path_obj.is_dir():
        logging.error(f"Source path is not a directory: {source_path}")
        return

    for filename in os.listdir(source_path):
        if is_image_file(filename):
            char_string = Path(filename).stem
            if char_string.isnumeric() and 0 <= int(char_string) < 0x110000:
                source_unicode_set.add(int(char_string))

def main(args: argparse.Namespace) -> None:
    """主函數。 """
    source_path = args.input
    filename_output = args.output
    source_unicode_set: Set[int] = set()

    if args.mode == "fontforge":
        process_font_file(source_path, source_unicode_set)
    elif args.mode == "unicode_image":
        process_image_folder(source_path, source_unicode_set)
    else:
        logging.error(f"Invalid mode: {args.mode}")
        return

    if source_unicode_set:
        source_name = Path(source_path).name
        if source_name.endswith(".sfdir"):
            source_name = source_name[:-6]
        filename_output = f"charset_{source_name}.txt" if filename_output == "output.txt" else filename_output

        save_set_to_file(source_unicode_set, filename_output)
        logging.info(f"Input: {source_path}")
        logging.info(f"Output: {filename_output}")
        logging.info(f"Charset length: {len(source_unicode_set)}")
    else:
        logging.warning("Source folder is empty!")

def cli() -> None:
    """命令行界面。 """
    parser = argparse.ArgumentParser(description="get ttf chars list")
    parser.add_argument("input", help=".otf / .ttf / .sfdir file path or image folder path", type=str)
    parser.add_argument("--output", help=".txt file path", default="output.txt", type=str)
    parser.add_argument("--mode", help="mode of folder (fontforge or unicode_image)", default="fontforge", type=str)
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()