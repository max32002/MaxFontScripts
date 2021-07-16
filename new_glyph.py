#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, isdir, isfile
import argparse

def new_glyph_file(output_folder, unicode_int, glyph_width, overwrite=False):
    unicode_hex = str(hex(unicode_int))[2:]
    filename = "uni%s.glyph" % (unicode_hex)
    output_filepath = join(output_folder, filename)
    print("save to filepath:", output_filepath)

    is_file_exist = isfile(output_filepath)
    is_write_file = True

    if not overwrite:
        if is_file_exist:
            is_write_file = False

    if not is_write_file:
        print("File exist, skip: %s" % (output_filepath))
    else:
        output_file = open(output_filepath, 'w')

        new_glyph = '''StartChar: uni%s
Encoding: %s %s 0
Width: %d
Flags: W
LayerCount: 2
Fore
SplineSet
EndSplineSet
EndChar''' % (unicode_hex.upper(), unicode_int, unicode_int, glyph_width)

        output_file.write(new_glyph)
        output_file.close()


def main():
    parser = argparse.ArgumentParser(description='anti aliasing')

    parser.add_argument("--output",
        help="output font folder",
        default=".",
        type=str)

    parser.add_argument("--string",
        help="input glyph chars list",
        required=True,
        type=str)

    parser.add_argument("--width",
        help="glyph width size",
        default=1024,
        type=int)

    parser.add_argument('--overwrite', 
        action='store_true'
        )

    args = parser.parse_args()

    output_folder = args.output
    chars = args.string
    glyph_width_int = args.width
    force_overwrite = args.overwrite

    #print("Open font:", image_file_in)
    #print("Save path:", image_file_out)

    if len(chars) > 0:
        for char in chars:
            unicode_int = -1
            if len(char) > 0:
                unicode_int = ord(char)
            new_glyph_file(output_folder, unicode_int, glyph_width_int, overwrite=force_overwrite)


if __name__ == '__main__':
    main()
