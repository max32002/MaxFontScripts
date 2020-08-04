#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import makedirs
from os.path import join, exists

# to copy file.
import shutil

import argparse

def copy_out(args):
    source_ff = args.input

    is_output_glyph = False     # view log only
    is_output_glyph = True      # get real file.

    upgrade_folder = args.output
    target_string = args.string
    string_file = args.file
    range_string = args.range
    #range_string_int = args.range_int
    range_string_int = None

    
    # from 1 to 3.
    #unicode_field = 2       # for Noto Sans
    unicode_field = args.unicode_field

    check_altuni2 = False
    if args.alt == "True":
        check_altuni2 = True

    # start to scan files.
    print("source project:", source_ff)
    print("output:", upgrade_folder)
    print("string length:", len(target_string))
    if not string_file is None:
        if len(string_file) > 0:
            print("string file:", string_file)
    if len(target_string) > 0 and len(target_string) <= 80:
        print("string:", target_string)
    if check_altuni2:
        print("check AltUni2")

    if len(target_string) == 0:
        # is need read from file.
        if len(string_file) > 0:
            if exists(string_file):
                my_list = []
                f = open(string_file,"r")
                file_raw_list = f.readlines()
                for line in file_raw_list:
                    line = line.strip()
                    for char in line:
                        if len(char) > 0:
                            my_list.append(char)
                f.close()
                target_string = ''.join(my_list)
                print("string length in file:", len(target_string))
            else:
                print("input file not exist:", string_file)

    if len(target_string) == 0:
        print("range:", range_string)
    if check_altuni2:
        print("check altuni2: True")

    source_unicode_set, source_dict = LibGlyph.load_files_to_set_dict(source_ff, unicode_field, check_altuni2)

    # source set from string.
    target_unicode_set = set()
    if not target_string is None:
        if len(target_string) > 0:
            for char in target_string:
                target_unicode_set.add(ord(char))

    # string 優先, 避免衝突。
    if len(target_unicode_set) == 0:
        if not range_string is None:
            if len(range_string) > 0:
                if ',' in range_string:
                    range_begin = range_string.split(',')[0]
                    range_end = range_string.split(',')[1]
                    for r in range(int(range_begin,16),int(range_end,16)+1):
                        target_unicode_set.add(r)

    if not range_string_int is None:
        if len(range_string_int) > 0:
            if ',' in range_string_int:
                range_begin = range_string_int.split(',')[0]
                range_end = range_string_int.split(',')[1]
                for r in range(int(range_begin),int(range_end)+1):
                    target_unicode_set.add(r)

    diff_set_common =  source_unicode_set & target_unicode_set

    print("length source project:", len(source_unicode_set))
    print("length selected string:", len(target_unicode_set))
    print("length intersection:", len(diff_set_common))

    if is_output_glyph:
        print("copy lost glyph file to path:", upgrade_folder)

        if not exists(upgrade_folder):
            makedirs(upgrade_folder)

        conflic_count = 0
        copy_count = 0
        for item in diff_set_common:

            source_path = join(source_ff,source_dict[item])
            #print("filename:", target_path)
            target_path = join(upgrade_folder,source_dict[item])
            if exists(target_path):
                print("conflic at path:", source_path)
                conflic_count += 1
            else:
                pass
            
            # force overwrite
            copy_count += 1
            shutil.copy(source_path,target_path)

        if conflic_count > 0:
            print("conflic count:", conflic_count)
        print("copy count:", copy_count)

def cli():
    parser = argparse.ArgumentParser(
            description="Get selected glyph from FontForge directory")

    parser.add_argument("--input",
        help="input more glyph font sfdir folder",
        required=True,
        type=str)

    parser.add_argument("--string",
        help="selected string",
        default='',
        type=str)

    parser.add_argument("--file",
        help="selected string file",
        default='',
        type=str)

    # CJK Radicals Supplement, U+2E80 - U+2EFF
    # 中日韓統一表意文字擴充區A, 3400 – U+4DBF
    # CJK Unified Ideographs, 4E00 - U+9FFF
    # CJK Compatibility Ideographs, U+F900 - U+FAFF
    # 中日韓統一表意文字擴充區B, U+20000 – U+2A6DF
    # 中日韓統一表意文字擴展區G, U+30000 – U+3134F
    # --range 20000,3134F
    #print("unicode_int:", unicode_int)
    #convert_range_list = [[13312,19903],[131072,201551]]
    parser.add_argument("--range",
        help="unicode range hex",
        default='',
        type=str)

    parser.add_argument("--range_int",
        help="unicode range integer",
        default='',
        type=str)

    parser.add_argument("--output",
        help="output glyth folder",
        default='.',
        type=str)

    parser.add_argument("--unicode_field",
        help="unicode_field in glyth",
        default=2,
        type=int)

    parser.add_argument("--log",
        help="generate log file",
        default="True",
        type=str)

    parser.add_argument("--alt",
        help="check AltUni2",
        default='False',
        type=str)

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()
