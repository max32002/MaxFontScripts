#!/usr/bin/env python3
#encoding=utf-8
import argparse
import platform
import os

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff', '.svg'}

def output_to_file(myfile, myfont_set):
    full_text = []
    for item in myfont_set:
        try:
            output_string = "%s" % (chr(item))
            full_text.append(output_string)
        except Exception as exc:
            print("error item:%d" %(item))
            print("error item(hex):%s" %(str(hex(item))))
            raise

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

    target_folder_list = os.listdir(source_folder)
    for filename in target_folder_list:
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path): # check if file
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension.lower()
            if file_extension in IMG_EXTENSIONS:
                char_string = os.path.splitext(filename)[0]
                if len(char_string) > 0:
                    if char_string.isnumeric():
                        char_int = int(char_string)
                        if char_int > 0 and char_int < 0x110000:
                            source_unicode_set.add(char_int)

    if len(source_unicode_set) > 0:
        source_name = os.path.basename(os.path.normpath(source_folder))
        if filename_output == "output.txt":
            filename_output = "charset_%s.txt" % source_name

        sorted_set=sorted(source_unicode_set)
        save_set_to_file(sorted_set, filename_output)

        print("input:", source_folder)
        print("output:", filename_output)
        print("charset length:", len(sorted_set))
    else:
        print("source folder is empty or no supported image files!")

def cli():
    parser = argparse.ArgumentParser(
        description="get ttf chars list from image files")

    parser.add_argument("--input",
        help="folder containing image files",
        type=str)

    parser.add_argument("--output",
        help=".txt file path",
        default="output.txt",
        type=str)

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()