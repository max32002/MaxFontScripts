#!/usr/bin/env python3
#encoding=utf-8

import argparse
import platform

def remove_out(args):
    input_charset = list(open(args.input, encoding='utf-8').readline().strip())
    print("length of input file:", len(input_charset))

    remove_charset = list(open(args.remove, encoding='utf-8').readline().strip())
    print("length of remove file:", len(remove_charset))

    formated_charset = []
    for ch in input_charset:
        if ch not in remove_charset:
            formated_charset.append(ch)
    print("excepted length of formated file:", len(input_charset) - len(remove_charset))
    print("length of formated file:", len(formated_charset))

    if len(formated_charset) > 0:
        filename_output = args.output
        outfile = None
        if platform.system() == 'Windows':
            outfile = open(filename_output, 'w', encoding='UTF-8')
        else:
            outfile = open(filename_output, 'w')
        outfile.write(''.join(formated_charset))
        outfile.close()
        outfile = None

def cli():
    parser = argparse.ArgumentParser(
            description="remove char")

    parser.add_argument("--input",
        help="input text file",
        required=True,
        type=str)

    parser.add_argument("--remove",
        help="string to remove",
        default='',
        type=str)

    parser.add_argument("--output",
        help="input text file",
        default="new.txt",
        type=str)

    args = parser.parse_args()
    remove_out(args)

if __name__ == "__main__":
    cli()
