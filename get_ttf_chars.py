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

IMG_EXTENSIONS = {'.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.BMP', '.TIF', '.TIFF'}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_image_file(filename: str) -> bool:
    """檢查文件是否為圖像文件。 """
    file_extension = Path(filename).suffix.upper()
    return file_extension in IMG_EXTENSIONS

def output_to_file(myfile, myfont_set: Set[int]) -> None:
    """將字符集輸出到文件。 """
    full_text: List[str] = []
    for item in sorted(myfont_set):
        try:
            output_string = chr(item)
            full_text.append(output_string)
        except ValueError as exc:
            logging.error(f"Error item: {item}, hex: {hex(item)}, error: {exc}")
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
    if any(source_path.endswith(ext) for ext in (".ttf", ".otf", ".woff", ".woff2")):
        if os.path.exists(source_path):
            try:
                myfont = fontforge.open(source_path)
                myfont.selection.all()
                all_glyph_list = list(myfont.selection.byGlyphs)
                for glyph in all_glyph_list:
                    char_int = glyph.unicode
                    if 0 < char_int <= 65536:
                        source_unicode_set.add(char_int)
            except Exception as e:
                logging.error(f"Error processing font file: {source_path}, error: {e}")
        else:
            logging.error(f"File not found: {source_path}")
    elif source_path.endswith(".sfdir"):
        try:
            import LibGlyph
            unicode_field = 2
            source_unicode_set.update(LibGlyph.load_files_to_set_dict(source_path, unicode_field)[0])
        except Exception as e:
            logging.error(f"Error processing sfdir: {source_path}, error: {e}")

def process_image_folder(source_path: str, source_unicode_set: Set[int]) -> None:
    """處理圖像文件夾。 """
    source_path_obj = Path(source_path)
    if not source_path_obj.is_dir():
        logging.error(f"Source path is not a directory: {source_path}")
        return
    for filename in os.listdir(source_path):
        if is_image_file(filename):
            char_string = Path(filename).stem
            if char_string.isnumeric():
                char_int = int(char_string)
                if 0 < char_int <= 65536:
                    source_unicode_set.add(char_int)

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
        if filename_output == "output.txt":
            filename_output = f"charset_{source_name}.txt"

        save_set_to_file(source_unicode_set, filename_output)
        logging.info(f"Input: {source_path}")
        logging.info(f"Output: {filename_output}")
        logging.info(f"Charset length: {len(source_unicode_set)}")
    else:
        logging.warning("Source folder is empty!")

def cli() -> None:
    """命令行界面。 """
    parser = argparse.ArgumentParser(description="get ttf chars list")
    parser.add_argument("--input", help=".otf / .ttf / .sfdir file path or image folder path", type=str)
    parser.add_argument("--output", help=".txt file path", default="output.txt", type=str)
    parser.add_argument("--mode", help="mode of folder (fontforge or unicode_image)", default="fontforge", type=str)
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()