#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, exists, isfile, islink, splitext
from pathlib import Path
import argparse

def update_block_between_files(first_path,second_path, begin_string, resume_string):
    output_debug_message = False
    #output_debug_message = True

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

    if output_debug_message:
        print("first part interrupt:", is_less_file_seeked_begin)

    # second part use more.
    is_more_file_seeked_begin = False
    x_line = more_file.readline()
    while x_line:
        if left_part_Second_Begin == x_line[:left_part_Second_Begin_length]:
            is_more_file_seeked_begin = True

        if left_part_First_Resume_length > 0:
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

    if output_debug_message:
        print("second part interrupt:", is_more_file_seeked_begin)

    # third part use less.
    is_our_line = False
    if left_part_First_Resume_length > 0:
        if is_less_file_seeked_begin and is_more_file_seeked_begin:
            x_line = less_file.readline()
            while x_line:
                if not is_our_line:
                    if left_part_First_Resume == x_line[:left_part_First_Resume_length]:
                        is_our_line = True

                if is_our_line:
                    output_file.write(x_line)

                x_line = less_file.readline()

    if output_debug_message:
        print("third part interrupt:", is_our_line)

    less_file.close()
    more_file.close()
    output_file.close()

    remove(first_path)
    rename(output_filepath, first_path)

def try_stat(path):
    ret = False
    from os import stat
    try:
        stat(path)
        ret = True
    except OSError as e:
        pass
    return ret

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

    is_pass_all_check = True
    if is_pass_all_check:
        # isfile will be False, if symlink
        # under symlink, all is false @_@;
        # please don't use under symlink.
        if False:
            print("exists(first_path)", exists(first_path))
            print("isfile(first_path)", isfile(first_path))
            print("islink(first_path)", islink(first_path))
            print("is_symlink(first_path)", Path(first_path).is_symlink())
            print('try_stat()',try_stat(first_path))

        if not exists(first_path):
            is_pass_all_check = False
            print("Error: first path not exists:", first_path)
        else:
            if not isfile(first_path):
                is_pass_all_check = False
                print("Error: first file not exists:", first_path)
    
    if is_pass_all_check:
        # under symlink, all is false @_@;
        # please don't use under symlink.
        if not exists(second_path):
            is_pass_all_check = False
            print("Error: second path not exists:", second_path)
        else:
            if not isfile(second_path):
                is_pass_all_check = False
                print("Error: second file not exists:", second_path)
    
    if is_pass_all_check:
        if len(begin_string) == 0:
            is_pass_all_check = False
            print("Error: begin string is empty!")

    if is_pass_all_check:
        update_block_between_files(first_path,second_path, begin_string, resume_string)
        update_file_count += 1
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
        default="",
        required=False,
        type=str)

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()
