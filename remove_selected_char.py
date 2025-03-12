#!/usr/bin/env python3
# encoding=utf-8

import argparse

def remove_out(args):
    try:
        with open(args.input, encoding='utf-8') as input_file:
            input_charset = set(input_file.readline().strip())

        with open(args.remove, encoding='utf-8') as remove_file:
            remove_charset = set(remove_file.readline().strip())

        diff_set_common = input_charset & remove_charset
        target_set = input_charset - diff_set_common
        sorted_set = sorted(target_set)
        formated_charset = ''.join(sorted_set)

        print("length of input file:", len(input_charset))
        print("length of remove file:", len(remove_charset))
        print("excepted length of formated file:", len(input_charset) - len(remove_charset))
        print("length intersection:", len(diff_set_common))
        print("length of target file:", len(target_set))

        if formated_charset:
            with open(args.output, 'w', encoding='utf-8') as outfile:
                outfile.write(formated_charset)

    except FileNotFoundError:
        print("Error: Input or remove file not found.")

def cli():
    parser = argparse.ArgumentParser(description="remove char")
    parser.add_argument("--input", help="input text file", required=True, type=str)
    parser.add_argument("--remove", help="string to remove", default='', type=str)
    parser.add_argument("--output", help="input text file", default="new.txt", type=str)

    args = parser.parse_args()
    remove_out(args)

if __name__ == "__main__":
    cli()