#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph
import os
import shutil
import argparse
import platform

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
    if check_altuni2:
        print("check AltUni2")

    if len(target_string) == 0:
        # is need read from file.
        if len(string_file) > 0:
            if os.path.exists(string_file):
                my_list = []
                f = None
                if platform.system() == 'Windows':
                    f = open(string_file, "r", encoding='UTF-8')
                else:
                    f = open(string_file, "r")
                if not f is None:
                    for line in f.readlines():
                        my_list.append(line.strip())
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
                # convert between symbole to ','
                if '-' in range_string:
                    range_string = range_string.replace('-',',')
                if '~' in range_string:
                    range_string = range_string.replace('~',',')
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

        if len(diff_set_common) > 0:
            if not os.path.exists(upgrade_folder):
                os.makedirs(upgrade_folder)

        conflic_count = 0
        copy_count = 0
        for item in diff_set_common:

            source_path = os.path.join(source_ff,source_dict[item])
            #print("filename:", target_path)
            target_path = os.path.join(upgrade_folder,source_dict[item])
            if os.path.exists(target_path):
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

    # --range AC00,D7AF
    '''
    2E80 - 2EFF: CJK Radicals Supplement
    3400 – 4DBF: 中日韓統一表意文字擴充區A, 
    4E00 - 9FFF: CJK Unified Ideographs, 
    AC00 — D7AF: 諺文音節 (Hangul Syllables), Hangul音節是一個Unicode塊，其中包含用於現代韓語的預先編寫的Hangul音節塊。音節可以通過算法直接映射到韓文字母Unicode塊中的兩個或三個字符的序列： U + 1100–U + 1112之一：19個現代韓文字母領先的輔音字母； U + 1161–U + 1175之一：21種現代韓文元音字母；
    F900 - FAFF: CJK Compatibility Ideographs
    20000 – 2A6DF: 中日韓統一表意文字擴充區B
    30000 – 3134F: 中日韓統一表意文字擴展區G    
    '''
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
