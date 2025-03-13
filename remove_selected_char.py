#!/usr/bin/env python3
# encoding=utf-8

import argparse

def process_sets(args):
    try:
        with open(args.input, encoding='utf-8') as input_file:
            input_charset = set(input_file.readline().strip())

        with open(args.remove, encoding='utf-8') as remove_file:
            remove_charset = set(remove_file.readline().strip())

        if args.mode in ["subtract", "sub", "-"]:
            target_set = input_charset - remove_charset
        elif args.mode in ["union", "add", "+"]:
            target_set = input_charset | remove_charset
        elif args.mode in ["intersect", "int", "&"]:
            target_set = input_charset & remove_charset
        else:
            print(f"Error: Invalid mode '{args.mode}'.")
            return

        sorted_set = sorted(target_set)
        formated_charset = ''.join(sorted_set)

        print("length of input file:", len(input_charset))
        print("length of remove file:", len(remove_charset))

        if args.mode in ["subtract", "sub", "-"]:
            print("excepted length of formated file:", len(input_charset) - len(remove_charset & input_charset))
        elif args.mode in ["union", "add", "+"]:
            print("excepted length of formated file:", len(input_charset | remove_charset))
        elif args.mode in ["intersect", "int", "&"]:
            print("excepted length of formated file:", len(input_charset & remove_charset))

        print("length of target file:", len(target_set))

        if formated_charset:
            with open(args.output, 'w', encoding='utf-8') as outfile:
                outfile.write(formated_charset)

    except FileNotFoundError:
        print("Error: Input or remove file not found.")

def cli():
    parser = argparse.ArgumentParser(description="process char sets")
    parser.add_argument("--input", help="input text file", required=True, type=str)
    parser.add_argument("--remove", help="string to process", required=True, type=str)
    parser.add_argument("--output", help="output text file", default="new.txt", type=str)
    parser.add_argument("--mode", help="mode of operation (subtract, union, intersect)", default="subtract", choices=["subtract", "sub", "-", "union", "add", "+", "intersect", "int", "&"], type=str)

    args = parser.parse_args()
    process_sets(args)

if __name__ == "__main__":
    cli()