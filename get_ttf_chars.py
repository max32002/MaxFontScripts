#!/usr/bin/env python3
#encoding=utf-8

import argparse
import platform
import LibGlyph

from os.path import join, exists, normpath, basename

def output_to_file(myfile, myfont_set):
    full_text = []
    for item in myfont_set:
        # filter
        if item < 13300:
            #continue
            pass
        
        if item > 65000:
            #continue
            pass
        
        try:
            #output_string = "%s(%s)" % (chr(item),str(hex(item))[2:])
            output_string = "%s" % (chr(item))
            #output_string = "%s\n" % (chr(item))
            #output_string = "%s " % (chr(item))
            #output_string = '"%s",' % (chr(item))
            full_text.append(output_string)
        except Exception as exc:
            print("error item:%d" %(item))
            print("error item(hex):%s" %(str(hex(item))))
            raise
            #pass
    myfile.write(''.join(full_text))

def get_ttf_chars_list(source_ff, unicode_field, filename_output):
    source_unicode_set, source_dict = LibGlyph.load_files_to_set_dict(source_ff, unicode_field)
    sorted_set=sorted(source_unicode_set)

    print("charset length:", len(source_unicode_set))
    #print("output compare result to file...")
    print("output file: %s" % filename_output)
    outfile = None
    if platform.system() == 'Windows':
        outfile = open(filename_output, 'w', encoding='UTF-8')
    else:
        outfile = open(filename_output, 'w')

    output_to_file(outfile ,sorted_set)
    outfile.close()
    outfile = None

def main(args):
    source_ff = args.input
    if not ".sfdir" in source_ff:
        source_ff += ".sfdir"

    source_name = (basename(normpath(source_ff)))
    if source_name.endswith(".sfdir"):
        source_name = source_name[:len(source_name)-6]
    filename_output = "charset_%s.txt" % source_name
    if args.output:
        filename_output = args.output
    print("input:", source_ff)
    print("output:", filename_output)

    # from 1 to 3.
    #unicode_field = 2       # for Noto Sans
    unicode_field = 2
    
    get_ttf_chars_list(source_ff, unicode_field, filename_output)

def cli():
    parser = argparse.ArgumentParser(
            description="get ttf chars list")

    parser.add_argument("--input",
        help=".sfdir file path",
        type=str)

    parser.add_argument("--output",
        help=".txt file path",
        type=str)
    
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()
