#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import listdir, remove
from os.path import join, exists

import argparse

# to copy file.
import shutil

def output_to_file(myfile, myfont_set):
    for item in myfont_set:
        try:
            output_string = "%s(%s)" % (chr(item),str(hex(item))[2:])
        except Exception as exc:
            print("error item:%d" %(item))
            print("error item(hex):%s" %(str(hex(item))))
            raise
            #pass
        myfile.write(output_string)

def copy_out(ff_folder, output_folder, source_string):
    # 指定要列出所有檔案的目錄
    source_unicode_set = set()

    if not source_string is None:
        for char in source_string:
            source_unicode_set.add(ord(char))


    #source_unicode_set, source_dict = LibGlyph.load_files_to_set_dict(source_ff)
    ff_unicode_set, ff_dict = LibGlyph.load_files_to_set_dict(ff_folder)

    print("length input string:", len(source_unicode_set))
    print("length target:", len(ff_unicode_set))
    diff_set_common =  ff_unicode_set & source_unicode_set
    print("length common:", len(diff_set_common))

    print("output compare result to file...")

    # copy source (lost) to upgrade folder
    conflic_count = 0
    copy_count = 0
    for item in diff_set_common:
        source_path = join(ff_folder,ff_dict[item])
        check_path = join(output_folder,ff_dict[item])
        target_path = check_path
        #print("filename:", target_path)
        if exists(check_path):
            output_string = "%s(%s)" % (chr(item),str(hex(item))[2:])
            print("conflic:", source_path, "for glyph:", item, "char:", output_string)
            conflic_count += 1

        shutil.copy(source_path, target_path)
        copy_count += 1

    print("conflic count:", conflic_count)
    print("copy count:", copy_count)


def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default='.',
        type=str)

    parser.add_argument("--text",
        help="lost char to auto compose",
        default='import.txt',
        type=str)

    parser.add_argument("--string",
        help="selected string",
        default='',
        type=str)

    args = parser.parse_args()

    # global setting.
    import_text = args.text
    working_ff = args.input
    target_ff = args.output
    user_string = args.string


    target_chars_list = []
    if exists(import_text):
        f = open(import_text,"r")
        target_chars_list = f.readlines()
        f.close()

    if len(user_string)==0:
        if exists(import_text):
            f = open(import_text,"r")
            file_raw_list = f.readlines()
            for line in file_raw_list:
                line = line.strip()
                for char in line:
                    if len(char) > 0:
                        user_string+=char
            f.close()

    copy_out(working_ff, target_ff, user_string)

if __name__ == "__main__":
    cli()
