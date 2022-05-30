#!/usr/bin/env python3
#encoding=utf-8

from os import remove, rename
from os.path import join, exists, splitext

import argparse

def get_current_char(l):
    s = l.split("char:")[1]
    s = s.split(" ")[0]
    return s

def scan_component_info(input_filepath, output_filepath):
    input_file = open(input_filepath, 'r')

    right_part_lost_char = ' is lost.\n'
    right_part_lost_char_length = len(right_part_lost_char)

    left_part_reset_string = "===="
    left_part_reset_string_length = len(left_part_reset_string)

    left_part_component_string = "component: "
    left_part_component_string_length = len(left_part_component_string)


    # scan lines
    current_char = ""
    component_1 = ""
    component_2 = ""
    component_dict = {}


    is_data_queued = False 

    x_line = input_file.readline()
    while x_line:
        if right_part_lost_char == x_line[-1 * right_part_lost_char_length:]:
            current_char = get_current_char(x_line)
            #print("match line:", x_line)
            #print("match char:", current_char)

        if left_part_component_string == x_line[:left_part_component_string_length]:
            c = x_line.split(" ")[1].strip()
            #print("match component:",c)
            if not (component_1 == ""):
                component_2 = c

            if component_2 == "":
                component_1 = c
            #print("match component 1:",component_1)
            #print("match component 2:",component_2)

        if left_part_reset_string == x_line[:left_part_reset_string_length]:
            #print("match reset.")
            # before reset, append to array.

            if len(component_1) > 0:
                if not component_1 in component_dict:
                    component_dict[component_1] = ""

                if not current_char in component_dict[component_1]:
                    component_dict[component_1] += current_char
                    is_data_queued = True
            
            if len(component_2) > 0:
                if not component_2 in component_dict:
                    component_dict[component_2] = ""

                if not current_char in component_dict[component_2]:
                    component_dict[component_2] += current_char
                    is_data_queued = True

            # start to reset.
            current_char = ""
            component_1 = ""
            component_2 = ""

        x_line = input_file.readline()

    input_file.close()


    # final data.
    if is_data_queued:
        output_file = open(output_filepath, 'w')
        format_count = 0
        for name, todo_list in component_dict.items():
            format_count += 1
            #print("%s: %s" % (name,todo_list))
            output_file.write("%s: %s\n" % (name,todo_list))
        output_file.close()

        print("%d rows output to file." % (format_count))
    else:
        print("No data output...")



def format_out(args):
    input_filepath = args.input
    output_filepath = args.output

    if output_filepath is None:
        output_filepath = "format_" + input_filepath

    # start to scan files.
    print("input text file:", input_filepath)
    print("output text file:", output_filepath)

    scan_component_info(input_filepath, output_filepath)

def cli():
    parser = argparse.ArgumentParser(
            description="Copy lost kerning info in glyphs to output folder")

    parser.add_argument("--input",
        help="your compose.log",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="formated compose.log",
        required=False,
        type=str)

    args = parser.parse_args()
    format_out(args)

if __name__ == "__main__":
    cli()
