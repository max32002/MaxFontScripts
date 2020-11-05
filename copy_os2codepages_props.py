#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, exists, splitext

import argparse

def update_kerning_info(less_path,more_path):
    output_filepath = less_path + ".tmp"

    less_file = open(less_path, 'r')
    more_file = open(more_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_LineGap = 'LineGap:'
    left_part_LineGap_length = len(left_part_LineGap)

    left_part_Lookup = 'Lookup:'
    left_part_Lookup_length = len(left_part_Lookup)

    # first part use less.
    is_less_file_seeked_begin = False
    x_line = less_file.readline()
    while x_line:
        if left_part_LineGap == x_line[:left_part_LineGap_length]:
            is_less_file_seeked_begin = True
            break
        output_file.write(x_line)
        x_line = less_file.readline()


    # second part use more.
    is_more_file_seeked_begin = False
    x_line = more_file.readline()
    while x_line:
        if left_part_LineGap == x_line[:left_part_LineGap_length]:
            is_more_file_seeked_begin = True

        if left_part_Lookup == x_line[:left_part_Lookup_length]:
            # more part, end here.
            break

        is_our_line = False
        if is_less_file_seeked_begin and is_more_file_seeked_begin:
            #print("both file seeked.")
            is_our_line = True
            
        if is_our_line:
            output_file.write(x_line)
        x_line = more_file.readline()

    # third part use less.
    if is_less_file_seeked_begin and is_more_file_seeked_begin:
        x_line = less_file.readline()
        is_our_line = False
        while x_line:
            if not is_our_line:
                if left_part_Lookup == x_line[:left_part_Lookup_length]:
                    is_our_line = True

            if is_our_line:
                output_file.write(x_line)

            x_line = less_file.readline()


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

    f = "font.props"
    less_path = join(less_ff,f)
    more_path = join(more_ff,f)

    file_count = 1
    update_file_count = 0
    if exists(more_path):
        print("less_path:", less_path)
        print("more_path:", more_path)
        update_kerning_info(less_path,more_path)
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
