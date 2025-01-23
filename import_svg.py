#!/usr/bin/env python3
#encoding=utf-8

import os
from os import mkdir
from os.path import exists, normpath, basename
import argparse

def import_svg(ff_path, out_path, svg_path, filename_pattern, filename_source, scale, simplify):
    print("Open font:", ff_path)
    print("Save dir:", out_path)
    print("Svg path:", svg_path)
    print("Filename pattern:", filename_pattern)
    print("Filename source:", filename_source)

    if len(ff_path) > 0:
        if ff_path[:1] == "/":
            ff_path = ff_path[:-1]

    if ff_path.endswith(".ttf"):
        font_name = (basename(normpath(ff_path)))
        project_path = font_name + ".sfdir"
        if out_path is None:
            out_path = project_path

    export_as_font = False

    if out_path is None:
        if ff_path.endswith(".ttf"):
            export_as_font = True
    else:
        if out_path.endswith(".ttf"):
            export_as_font = True

    if not out_path is None:
        if out_path.endswith(".sfdir"):
            if not exists(out_path):
                mkdir(out_path)

    myfont=fontforge.open(ff_path)
    myfont.selection.all()

    skip_list = []

    import_counter = 0
    import_char_list = ""
    
    idx = 0
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

        if debug:
            print("svg path:", svg_filepath)
            print("filename:", filename)
            print("filename_variable:", filename_variable)

        if exists(svg_filepath):
            if debug:
                print("found matched svg path: %s" % (svg_filepath) )

            glyph.clear()
            glyph.importOutlines(svg_filepath, scale=scale, simplify=simplify)
            glyph.width = previous_width
            import_counter += 1
            import_char_list += chr(unicode_int)

        if idx % 1000 == 0:
            print("Processing (%d)export" % (idx))

    formated_imported_text = import_char_list
    if len(formated_imported_text) > 300:
        formated_imported_text = formated_imported_text[:40] + "..." + formated_imported_text[-40:]
    print("Source font glyph count:", idx)
    print("Imported count:", import_counter)
    #print("Imported text:", formated_imported_text)

    if import_counter > 0:
        if export_as_font:
            myfont.generate(out_path)
        else:
            if out_path is None:
                myfont.save()
            else:
                myfont.save(out_path)
    else:
        print("Do nothing due to no changed glyph.")

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
        default="unicode_int",
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
