#!/usr/bin/env python3
#encoding=utf-8
import os
import shutil
import argparse
import platform

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff', '.svg'}

def copy_out(args):
    source_folder = args.input
    target_output = args.output
    target_string = args.string
    string_file = args.file
    range_string = args.range
    range_string_int = args.range_int
    mode = args.mode

    print("Source folder:", source_folder)
    print("Output folder:", target_output)
    print("String length:", len(target_string))

    if string_file:
        print("String file:", string_file)
        if not os.path.exists(string_file):
            print(f"Input file not exist: {string_file}")
        else:
            try:
                with open(string_file, "r", encoding='UTF-8' if platform.system() == 'Windows' else 'r') as f:
                    target_string = ''.join(line.strip() for line in f)
                print("String length in file:", len(target_string))
            except Exception as e:
                print(f"Error reading file: {string_file}, {e}")

    target_unicode_set = {ord(char) for char in target_string}

    if not target_unicode_set and range_string:
        range_string = range_string.replace('-', ',').replace('~', ',')
        if ',' in range_string:
            try:
                range_begin, range_end = range_string.split(',')
                target_unicode_set.update(range(int(range_begin, 16), int(range_end, 16) + 1))
            except ValueError:
                print(f"Invalid range string: {range_string}")

    if not target_unicode_set and range_string_int:
        if ',' in range_string_int:
            try:
                range_begin, range_end = range_string_int.split(',')
                target_unicode_set.update(range(int(range_begin), int(range_end) + 1))
            except ValueError:
                print(f"Invalid range integer string: {range_string_int}")

    source_dict = {}
    source_unicode_set = set()

    if mode == "unicode_image":
        target_folder_list = os.listdir(source_folder)
        for filename in target_folder_list:
            file_path = os.path.join(source_folder, filename)
            if os.path.isfile(file_path):
                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension.lower()
                if file_extension in IMG_EXTENSIONS:
                    char_string = os.path.splitext(filename)[0]
                    if char_string.isnumeric() and 0 < int(char_string) < 0x110000:
                        char_int = int(char_string)
                        source_unicode_set.add(char_int)
                        source_dict[char_int] = filename

    diff_set_common = source_unicode_set & target_unicode_set

    print("Length source folder:", len(source_unicode_set))
    print("Length selected string:", len(target_unicode_set))
    print("Length intersection:", len(diff_set_common))

    if diff_set_common:
        print(f"Copy lost glyph file to path: {target_output}")
        os.makedirs(target_output, exist_ok=True)

        conflic_count = 0
        copy_count = 0
        for item in diff_set_common:
            source_path = os.path.join(source_folder, source_dict[item])
            target_path = os.path.join(target_output, source_dict[item])
            if os.path.exists(target_path):
                print(f"Conflict at path: {source_path}")
                conflic_count += 1
            shutil.copy(source_path, target_path)
            copy_count += 1

        if conflic_count > 0:
            print(f"Conflict count: {conflic_count}")
        print(f"Copy count: {copy_count}")
    else:
        print("No matching glyphs found.")

def cli():
    parser = argparse.ArgumentParser(
        description="Get selected glyph from FontForge directory")

    parser.add_argument("--input", required=True, help="Input more glyph font sfdir folder", type=str)
    parser.add_argument("--string", help="Selected string", default='', type=str)
    parser.add_argument("--file", help="Selected string file", default='', type=str)
    parser.add_argument("--range", help="Unicode range hex", default='', type=str)
    parser.add_argument("--range_int", help="Unicode range integer", default='', type=str)
    parser.add_argument("--output", help="Output file folder", default='output', type=str)
    parser.add_argument("--mode", help="Mode of folder", default="unicode_image", type=str)

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()