#!/usr/bin/env python3
#encoding=utf-8

import os
from os import mkdir
from os.path import exists
import argparse

def import_svg(ff_tmp, out_path, svg_path, filename_pattern, filename_source, scale, simplify):
    print("Open font:", ff_tmp)
    print("Save dir:", out_path)
    print("Svg path:", svg_path)
    print("Filename pattern:", filename_pattern)
    print("Filename source:", filename_source)

    '''
scale (boolean, default=True)
Scale imported images and SVGs to ascender height

simplify (boolean, default=True)
Run simplify on the output of stroked paths

accuracy (float, default=0.25)
The minimum accuracy (in em-units) of stroked paths.

default_joinlimit (float, default=-1)
Override the format’s default miterlimit for stroked paths, which is 10.0 for PostScript and 4.0 for SVG. (Value -1 means “inherit” those defaults.)

handle_eraser (boolean, default=False)
Certain programs use pens with white ink as erasers. When this flag is set FontForge will attempt to simulate that.

correctdir (boolean, default=False)
Run “Correct direction” on (some) PostScript paths

usesystem (boolean, default=False)
Ignore the above keyword settings and use the values set by the user in the Import options dialog.

asksystem (boolean, default=False)
If the UI is present show the Import options dialog to the user and use the chosen values (does nothing otherwise).
    '''

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
            glyph.importOutlines(svg_filepath, scale=scale, simplify=simplify)
            glyph.width = previous_width
            import_counter += 1
            import_char_list += chr(unicode_int)

        if debug:
            if unicode_int == debug_char_int:
                print("match debug char ... end")

        if idx % 1000 == 0:
            print("Processing (%d)export: %d" % (idx, import_counter))

    formated_imported_text = import_char_list
    if len(formated_imported_text) > 300:
        formated_imported_text = formated_imported_text[:40] + "..." + formated_imported_text[-40:]
    print("Done,\nImported count:%d \nImported text:%s\n" % (import_counter, formated_imported_text))

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

    parser.add_argument('--disable_scale', 
        help='disable to scale imported images and SVGs to ascender height',
        action='store_true'
        )
    parser.add_argument('--disable_simplify', 
        help='disable to simplify on the output of stroked paths',
        action='store_true'
        )

    args = parser.parse_args()

    project_output = args.input
    
    if not args.output is None:
        project_output = args.output

    scale = True
    if args.disable_scale:
        scale = False

    simplify = True
    if args.disable_simplify:
        simplify = False


    pass_precheck = True
    
    if not exists(args.svg_path):
        pass_precheck = False
        print("svg path not found: %s" % (args.svg_path))

    if pass_precheck:
        import_svg(args.input, project_output, args.svg_path, args.filename_pattern, args.filename_source, scale, simplify)

if __name__ == "__main__":
    cli()
