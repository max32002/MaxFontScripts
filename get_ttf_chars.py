#!/usr/bin/env python3
#encoding=utf-8

import argparse
import platform
import LibGlyph
import os
from os.path import normpath, basename

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


def save_set_to_file(sorted_set, filename_output):
    outfile = None
    if platform.system() == 'Windows':
        outfile = open(filename_output, 'w', encoding='UTF-8')
    else:
        outfile = open(filename_output, 'w')

    output_to_file(outfile ,sorted_set)
    outfile.close()
    outfile = None

def main(args):
    source_folder = args.input
    filename_output = args.output
    source_unicode_set = set()

    if args.mode == "fontforge":
        if not ".sfdir" in source_folder:
            source_folder += ".sfdir"

        # from 1 to 3.
        #unicode_field = 2       # for Noto Sans
        unicode_field = 2
        
        source_unicode_set, source_dict = LibGlyph.load_files_to_set_dict(source_folder, unicode_field)

    if args.mode == "unicode_image":
        target_folder_list = os.listdir(source_folder)
        for filename in target_folder_list:
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                #print("image file name", filename)
                char_string = os.path.splitext(filename)[0]
                if len(char_string) > 0:
                    #print("char_string", char_string)
                    #source_unicode_set.add(chr(int(char_string)))
                    source_unicode_set.add(int(char_string))
    
    if len(source_unicode_set) > 0:
        source_name = (basename(normpath(source_folder)))
        if source_name.endswith(".sfdir"):
            source_name = source_name[:len(source_name)-6]
        if filename_output == "output.txt":
            filename_output = "charset_%s.txt" % source_name

        sorted_set=sorted(source_unicode_set)
        save_set_to_file(sorted_set, filename_output)

        print("input:", source_folder)
        print("output:", filename_output)
        print("charset length:", len(sorted_set))
    else:
        print("source folder is empty!")

def cli():
    parser = argparse.ArgumentParser(
            description="get ttf chars list")

    parser.add_argument("--input",
        help=".sfdir file path",
        type=str)

    parser.add_argument("--output",
        help=".txt file path",
        default="output.txt", 
        type=str)
    
    parser.add_argument("--mode",
        help="mode of folder",
        default="fontforge", 
        type=str)

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()
