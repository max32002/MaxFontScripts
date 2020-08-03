#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, exists, splitext

import argparse

def update_kerning_info(first_path,second_path, begin_string, resume_string):
    output_filepath = first_path + ".tmp"

    less_file = open(first_path, 'r')
    more_file = open(second_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_Second_Begin = begin_string
    left_part_Second_Begin_length = len(left_part_Second_Begin)

    left_part_First_Resume = resume_string
    left_part_First_Resume_length = len(left_part_First_Resume)


    # first part use less.
    is_less_file_seeked_begin = False
    x_line = less_file.readline()
    while x_line:
        if left_part_Second_Begin == x_line[:left_part_Second_Begin_length]:
            is_less_file_seeked_begin = True
            break
        output_file.write(x_line)
        x_line = less_file.readline()


    # second part use more.
    is_more_file_seeked_begin = False
    x_line = more_file.readline()
    while x_line:
        if left_part_Second_Begin == x_line[:left_part_Second_Begin_length]:
            is_more_file_seeked_begin = True

        if left_part_First_Resume == x_line[:left_part_First_Resume_length]:
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
                if left_part_First_Resume == x_line[:left_part_First_Resume_length]:
                    is_our_line = True

            if is_our_line:
                output_file.write(x_line)

            x_line = less_file.readline()


    less_file.close()
    more_file.close()
    output_file.close()

    remove(first_path)
    rename(output_filepath, first_path)

def copy_out(args):
    second_path, first_path = args.second, args.first
    begin_string, resume_string = args.begin, args.resume

    # start to scan files.
    print("first file:", first_path)
    print("second file:", second_path)
    print("begin_string:", begin_string)
    print("resume_string:", resume_string)

    file_count = 1
    update_file_count = 0
    if exists(first_path) and exists(second_path):
        update_kerning_info(first_path,second_path, begin_string, resume_string)
        update_file_count += 1
    else:
        print("some file not exists.")

    print("check file count:",file_count)
    print("update file count:",update_file_count)

def cli():
    parser = argparse.ArgumentParser(
            description="Copy lost kerning info in glyphs to output folder")

    parser.add_argument("--first",
        help="first file path, will be updated.",
        required=True,
        type=str)

    parser.add_argument("--second",
        help="second file path, content weill be copied.",
        required=True,
        type=str)

    parser.add_argument("--begin",
        help="second file begin string",
        required=True,
        type=str)

    parser.add_argument("--resume",
        help="first file resume string",
        required=True,
        type=str)

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()
