#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, isdir, isfile

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


if __name__ == '__main__':
    #prefix_string = "Baku"

    import sys
    argument_count = 4
    if len(sys.argv)==argument_count:
        output_folder = sys.argv[1]
        chars = sys.argv[2]
        glyph_width = sys.argv[3]
        force_overwrite = False
        
        if len(chars) > 0:
            for char in chars:
                unicode_int = -1
                glyph_width_int = 1024
                
                if len(char) > 0:
                    unicode_int = ord(char)
                if len(glyph_width) > 0:
                    glyph_width_int = int(glyph_width)
                
                
                new_glyph_file(output_folder, unicode_int, glyph_width_int, overwrite=force_overwrite)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s output_folder chars glyph_width" % (sys.argv[0]))


