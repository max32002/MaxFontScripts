#!/usr/bin/env python3
#encoding=utf-8

from os import remove, rename
from os.path import join, exists

import argparse


# return:
#   True, append successfully.
#   False, do nothing.
def update_family_tags(config_path):
    ret = False

    output_filepath = config_path + ".tmp"

    input_file = open(config_path, 'r')
    output_file = open(output_filepath, 'w')

    
    left_part_FullName = 'FullName:'
    left_part_FullName_length = len(left_part_FullName)

    left_part_FamilyName = 'FamilyName:'
    left_part_FamilyName_length = len(left_part_FamilyName)

    left_part_LangName = 'LangName: 1033'
    left_part_LangName_length = len(left_part_LangName)

    right_part_LangName = "\"http://scripts.sil.org/OFL\""
    right_part_LangName_length = len(right_part_LangName)


    is_weight_found = False
    is_title_found = False

    font_weight = ""
    font_title = ""

    # get title.

    x_line = input_file.readline()
    while x_line:
        formated_x_line = x_line

        if left_part_FullName == x_line[:left_part_FullName_length]:

            field_right_part = x_line[left_part_FullName_length:].strip()
            if ' ' in field_right_part:
                font_weight_array = field_right_part.split(' ')
                font_weight = font_weight_array[len(font_weight_array)-1]
                is_weight_found = True
                print("Font Weight:", font_weight)

        if left_part_FamilyName == x_line[:left_part_FamilyName_length]:
            is_title_found = True

            font_title = x_line[left_part_FamilyName_length:]
            font_title = font_title.strip()
            print("Font Title:", font_title)
            #break

        # append to string.
        if is_title_found and is_weight_found:
            if left_part_LangName == x_line[:left_part_LangName_length]:
                formated_x_line = formated_x_line.strip()
                if right_part_LangName == formated_x_line[-1 * right_part_LangName_length:]:
                    print("Found empty language, append prefer family tag now...")
                    formated_x_line += " \"\" \"%s\" \"%s\"\n" % (font_title, font_weight)
                    ret = True

        x_line = input_file.readline()
        output_file.write(formated_x_line)



    input_file.close()
    output_file.close()

    if ret:
        remove(config_path)
        rename(output_filepath, config_path)
    else:
        # clean tmp file.
        remove(output_filepath)

    return ret

def append_family_tags(args):
    from_ff = args.input

    print("input project:", from_ff)
    config_path = ""

    # join font.props, or skip.
    f = "font.props"
    f_length = len(f)
    if from_ff[-1*f_length:] != f:
        config_path = join(from_ff,f)
    else:
        config_path = from_ff

    if exists(config_path):
        ret = update_family_tags(config_path)
        if not ret:
            print("Nothing modified.")
    else:
        print("error, font.props path not found:", config_path)

def cli():
    parser = argparse.ArgumentParser(
            description="add prefer family for english")

    parser.add_argument("--input",
        help="input font sfdir folder",
        default=".",
        type=str)

    args = parser.parse_args()
    append_family_tags(args)
    print("Done.")

if __name__ == "__main__":
    cli()
