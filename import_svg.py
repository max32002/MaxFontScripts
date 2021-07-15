#!/usr/bin/env python3
#encoding=utf-8

import os
from os import mkdir
from os.path import exists
import argparse

def import_svg(ff_tmp, out_path, svg_path, filename_pattern, filename_source):
    print("Open font:", ff_tmp)
    print("Save dir:", out_path)
    print("Svg path:", svg_path)
    print("Filename pattern:", filename_pattern)
    print("Filename source:", filename_source)

    if not exists(out_path):
        mkdir(out_path)
    else:
        pass

    myfont=fontforge.open(ff_tmp)
    myfont.selection.all()

    idx = 0

    skip_list = []

    # read chars list from text.
    #for char in mychars:
        #myfont.selection.select(ord(char))

    import_counter = 0
    import_char_list = ""
    for glyph in myfont.selection.byGlyphs:
        idx +=1

        #unicode_string = str(hex(glyph.unicode))[2:]
        unicode_int = glyph.unicode
        if unicode_int in skip_list:
            continue

        if unicode_int <= 0:
            continue

        previous_width = glyph.width
        if glyph.width <= 0:
            continue

        # default use 'char'
        filename_variable = chr(unicode_int)
        if filename_source == 'unicode_hex':
            filename_variable = str(hex(unicode_int))[2:]
        if filename_source == 'unicode_int':
            filename_variable = unicode_int
        filename=filename_pattern % (filename_variable)
        svg_filepath = os.path.join(svg_path,filename)

        debug = False       # online
        #debug = True
        debug_char = "乩"
        debug_char_int = ord(debug_char)

        if debug:
            if unicode_int == debug_char_int:
                print("match debug char ... start")
                print("debug svg path:", svg_filepath)

        if exists(svg_filepath):
            if debug:
                print("found matched svg path: %s" % (svg_filepath) )
            glyph.clear()
            glyph.importOutlines(svg_filepath)
            glyph.width = previous_width
            import_counter += 1
            import_char_list += chr(unicode_int)

        if debug:
            if unicode_int == debug_char_int:
                print("match debug char ... end")

        if idx % 1000 == 0:
            print("Processing (%d)export: %d" % (idx, import_counter))

    print("Done,\nImported count:%d \nImported text:%s\n" % (import_counter, import_char_list))

    if import_counter > 0:
        myfont.save(out_path)

def cli():
    parser = argparse.ArgumentParser(
            description="import svg to font")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default=None,
        type=str)

    parser.add_argument("--svg_path",
        help="import svg folder",
        default=".",
        type=str)

    parser.add_argument("--filename_pattern",
        help="svg filename pattern",
        default="%s.svg",
        type=str)
    
    parser.add_argument("--filename_source", type=str, choices=['char', 'unicode_hex', 'unicode_int'],
        help='svg filename pattern source.\n'
             'use char for character.\n'
             'use unicode_hex for unicode hex .\n'
             'use unicode_hex for unicode decimal.',
        default="char",
        )

    args = parser.parse_args()

    project_output = args.input
    
    if not args.output is None:
        project_output = args.output

    pass_precheck = True
    
    if not exists(args.svg_path):
        pass_precheck = False
        print("svg path not found: %s" % (args.svg_path))

    if pass_precheck:
        import_svg(args.input, project_output, args.svg_path, args.filename_pattern, args.filename_source)

if __name__ == "__main__":
    cli()
