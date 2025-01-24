#!/usr/bin/env python3
#encoding=utf-8

import os
from os import mkdir
from os.path import exists, normpath, basename
import argparse

def import_main(args):
    ff_path = args.input
    out_path = args.output

    scale = False
    if args.enable_scale:
        scale = True

    simplify = True
    if args.disable_simplify:
        simplify = False

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
        if ff_path.endswith(".ttf") or ff_path.endswith(".woff") or ff_path.endswith(".woff2"):
            export_as_font = True
    else:
        if out_path.endswith(".ttf") or out_path.endswith(".woff") or out_path.endswith(".woff2"):
            export_as_font = True

    if not out_path is None:
        if out_path.endswith(".sfdir"):
            if not exists(out_path):
                mkdir(out_path)

    print("Open font:", ff_path)
    print("Save dir:", out_path)
    print("Svg path:", args.svg_path)
    print("Filename pattern:", args.filename_pattern)
    print("Filename source:", args.filename_source)

    if exists(ff_path):
        myfont=fontforge.open(ff_path)
        myfont, import_char_list = import_svg(myfont, args.svg_path, args.filename_pattern, args.filename_source, scale, simplify, args.begin, args.end)

        # font config.
        if not args.comment is None:
            myfont.comment = args.comment
        if not args.familyname is None:
            myfont.familyname = args.familyname
        if not args.fontname is None:
            myfont.fontname = args.fontname
        if not args.fullname is None:
            myfont.fullname = args.fullname
        if not args.macstyle is None:
            myfont.macstyle = args.macstyle
        if not args.weight is None:
            myfont.weight = args.weight

        if len(import_char_list) > 0:
            if export_as_font:
                myfont.generate(out_path)
            else:
                if out_path is None:
                    myfont.save()
                else:
                    myfont.save(out_path)
        else:
            print("Do nothing due to no changed glyph.")

def import_svg(myfont, svg_path, filename_pattern, filename_source, scale, simplify, index_begin=0, index_end=99999):

    myfont.selection.all()

    skip_list = []
    import_char_list = set()
    fail_char_list = set()

    all_glyph_list = list(myfont.selection.byGlyphs)
    print("Source font total glyph:", len(all_glyph_list))
    
    idx = 0
    for glyph in all_glyph_list:
        idx +=1
        
        unicode_int = glyph.unicode
        if unicode_int in skip_list:
            continue

        if unicode_int <= 0:
            continue

        current_glyph_width = glyph.width
        if glyph.width <= 0:
            continue

        if idx < index_begin:
            continue

        if idx > index_end:
            continue

        # altuni, cause glyph expand stroke more times.
        if glyph.changed:
            continue

        # due to error:
        # internal buffer error : Memory allocation failed : growing buffer
        # I/O error : Memory allocation failed : growing input buffer

        filename_variable = chr(unicode_int)
        if glyph.originalgid in import_char_list:
            #print("duplicated char due to altuni:", filename_variable, "id:", glyph.originalgid)
            continue

        if filename_source == 'unicode_hex':
            filename_variable = str(hex(unicode_int))[2:]
        if filename_source == 'unicode_int':
            filename_variable = unicode_int
        filename=filename_pattern % (filename_variable)
        svg_filepath = os.path.join(svg_path,filename)

        debug = False       # online
        #debug = True

        if debug:
            print("-"*20)
            print("glyph originalgid:", glyph.originalgid)
            print("glyph unicode:", unicode_int)
            print("glyph altuni:", glyph.altuni)
            print("glyph char:", chr(unicode_int))

            print("svg path:", svg_filepath)
            print("filename:", filename)
            print("filename_variable:", filename_variable)


        if not exists(svg_filepath):
            if not glyph.altuni is None:
                for altuni_tuple in glyph.altuni:
                    #print("glyph altuni_tuple:", altuni_tuple)
                    unicode_value = 0
                    try:
                        (unicode_value, variation_selector, reserved_field) = altuni_tuple
                    except Exception as exc:
                        #print("glyph altuni:", glyph.altuni)
                        print(exc)
                        pass

                    if unicode_value > 0:
                        #print("glyph unicode_value:", unicode_value)
                        filename=filename_pattern % (str(unicode_value))
                        svg_filepath = os.path.join(svg_path,filename)
                        #print("new svg path:", svg_filepath)
                        if exists(svg_filepath):
                            break

        if exists(svg_filepath):
            if debug:
                print("found matched svg path: %s" % (svg_filepath) )

            try:
                glyph.clear()
                glyph.importOutlines(svg_filepath, scale=scale, simplify=simplify)
                glyph.width = current_glyph_width
                
                import_char_list.add(glyph.originalgid)
            except Exception as exc:
                fail_char_list.add(unicode_int)
                print("error svg path:", svg_filepath)
                print(exc)
                pass

        if idx % 1000 == 0:
            print("Processing glyph: %d" % (idx))

    print("Imported count:", len(import_char_list))
    #print("Imported text:", formated_imported_text)
    if len(fail_char_list) > 0:
        print("Failed count:", len(fail_char_list))
        print("Failed char:", fail_char_list)

    return myfont, import_char_list


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

    parser.add_argument('--enable_scale', 
        help='enable to scale imported images and SVGs to ascender height',
        action='store_true'
        )
    parser.add_argument('--disable_simplify', 
        help='disable to simplify on the output of stroked paths',
        action='store_true'
        )

    parser.add_argument('--begin', type=int, default=0)
    parser.add_argument('--end', type=int, default=99999)

    # font config.
    parser.add_argument("--comment",
        help="A comment associated with the font. Can be anything.",
        type=str)

    parser.add_argument("--familyname",
        help="PostScript font family name",
        type=str)

    parser.add_argument("--fontname",
        help="PostScript font name",
        type=str)

    parser.add_argument("--fullname",
        help="PostScript font name",
        type=str)

    parser.add_argument("--macstyle",
        help="Bold (if set to 1)",
        type=int)

    parser.add_argument("--weight",
        help="PostScript font weight string",
        type=str)

    # convert name list.
    parser.add_argument("--namelist",
        help="namelist string",
        default="",
        type=str)


    args = parser.parse_args()

    pass_precheck = True
    
    if not exists(args.svg_path):
        pass_precheck = False
        print("svg path not found: %s" % (args.svg_path))

    if pass_precheck:
        import_main(args)

if __name__ == "__main__":
    cli()
