#!/usr/bin/env python3
#encoding=utf-8

import argparse
import platform

def remove_out(args):
    input_charset = list(open(args.input, encoding='utf-8').readline().strip())

    remove_charset = list(open(args.remove, encoding='utf-8').readline().strip())

    source_unicode_set = set()
    for char in input_charset:
        source_unicode_set.add(ord(char))

    remove_unicode_set = set()
    for char in remove_charset:
        remove_unicode_set.add(ord(char))

    diff_set_common =  source_unicode_set & remove_unicode_set
    
    print("length of input file:", len(input_charset))
    print("length of remove file:", len(remove_charset))
    print("excepted length of formated file:", len(input_charset) - len(remove_charset))
    print("length intersection:", len(diff_set_common))

    target_set = source_unicode_set - diff_set_common
    sorted_set=sorted(target_set)
    formated_charset = []
    for char in sorted_set:
        formated_charset.append(chr(char))
    print("length of target file:", len(target_set))
    #print("data:", formated_charset)

    if len(formated_charset) > 0:
        final_string =''.join(formated_charset) 
        #print("final string:", final_string)

        filename_output = args.output
        outfile = None
        if platform.system() == 'Windows':
            outfile = open(filename_output, 'w', encoding='UTF-8')
        else:
            outfile = open(filename_output, 'w')
        outfile.write(final_string)
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
