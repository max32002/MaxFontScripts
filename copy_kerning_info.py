#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, exists, splitext

import argparse

def append_kerning_info(less_path,more_path):
    output_filepath = less_path + ".tmp"

    less_file = open(less_path, 'r')
    more_file = open(more_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_EndSplineSet = 'EndSplineSet'
    left_part_EndSplineSet_length = len(left_part_EndSplineSet)

    is_less_file_seeked = False
    x_line = less_file.readline()
    while x_line:
        if left_part_EndSplineSet == x_line[:left_part_EndSplineSet_length]:
            is_less_file_seeked = True
            break
        output_file.write(x_line)
        x_line = less_file.readline()


    is_more_file_seeked = False
    x_line = more_file.readline()
    while x_line:
        if left_part_EndSplineSet == x_line[:left_part_EndSplineSet_length]:
            is_more_file_seeked = True

        is_our_line = False
        if is_less_file_seeked and is_more_file_seeked:
            #print("both file seeked.")
            is_our_line = True
            
            # we change namelist to AGL new font.
            if 'Identity.' in x_line:
                is_our_line = False
            # skip 'vpal' / 'palt'
            if "'vpal'" in x_line:
                #is_our_line = False
                pass
            if "'palt'" in x_line:
                #is_our_line = False
                pass

        if is_our_line:
            output_file.write(x_line)
        x_line = more_file.readline()


    less_file.close()
    more_file.close()
    output_file.close()

    remove(less_path)
    rename(output_filepath, less_path)

def copy_out(args):
    more_ff, less_ff = args.more, args.less

    # start to scan files.
    print("more project:", more_ff)
    print("less project:", less_ff)

    files = listdir(less_ff)
    file_count = 0
    update_file_count = 0
    for f in files:
        file_count += 1

        # must match extension only, exclude ".extension.tmp" file.
        extension = splitext(f)
        #print("extension:", extension[1])
        #break

        if extension[1] == '.glyph':
            # skip hidden files.
            if f[:1] == ".":
                #continue
                pass

            if f == "nonmarkingreturn.glyph":
                #continue
                pass
                
            less_path = join(less_ff,f)
            more_path = join(more_ff,f)
            if exists(more_path):
                #print("less_path:", less_path)
                #print("more_path:", more_path)
                append_kerning_info(less_path,more_path)
                update_file_count += 1
    print("check file count:",file_count)
    print("update file count:",update_file_count)

def cli():
    parser = argparse.ArgumentParser(
            description="Copy lost kerning info in glyphs to output folder")

    parser.add_argument("--more",
        help="more glyph font sfdir folder",
        required=True,
        type=str)

    parser.add_argument("--less",
        help="less glyph font sfdir folder",
        required=True,
        type=str)

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()
