#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import exists, normpath, basename
import argparse

def font_delete_font_main(args):
    ff_path = args.input
    remove_path = args.remove
    out_path = args.output

    if len(ff_path) > 0:
        if ff_path[:1] == "/":
            ff_path = ff_path[:-1]

    if ff_path.endswith(".ttf"):
        font_name = basename(normpath(ff_path))
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

    print("Input font:", ff_path)
    print("Removed font:", remove_path)
    print("Save font:", out_path)

    if exists(ff_path) and exists(remove_path):
        myfont=fontforge.open(ff_path)
        
        removefont=fontforge.open(remove_path)
        target_charset_list = get_glyph_list(removefont)
        print('length of remove target count:', len(target_charset_list))

        myfont, cleared_char_list = clear_glyph(myfont, target_charset_list)
        print("Cleared count:", len(cleared_char_list))

        if len(cleared_char_list) > 0:
            if export_as_font:
                myfont.generate(out_path)
            else:
                if out_path is None:
                    myfont.save()
                else:
                    myfont.save(out_path)
        else:
            print("Do nothing due to no changed glyph.")

def get_glyph_list(myfont):
    myfont.selection.all()
    charset_list = set()
    all_glyph_list = list(myfont.selection.byGlyphs)
    idx = 0
    for glyph in all_glyph_list:
        idx +=1
        unicode_int = glyph.unicode
        if unicode_int <= 0:
            continue
        if glyph.width <= 0:
            continue
        charset_list.add(unicode_int)
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
                    charset_list.add(unicode_value)
    return charset_list

def clear_glyph(myfont, selected_chars):
    myfont.selection.all()
    all_glyph_list = list(myfont.selection.byGlyphs)
    cleared_char_list = set()
    idx = 0
    for glyph in all_glyph_list:
        idx +=1
        unicode_int = glyph.unicode
        if unicode_int <= 0:
            continue
        if glyph.width <= 0:
            continue
        if unicode_int in selected_chars:
            glyph.clear()
            cleared_char_list.add(unicode_int)
        if idx % 1000 == 0:
            print("Processing glyph: %d" % (idx))
    return myfont, cleared_char_list


def cli():
    parser = argparse.ArgumentParser(
            description="clear glyph from font")

    parser.add_argument("--input",
        help="input font project or file",
        required=True,
        type=str)

    parser.add_argument("--remove",
        help="clear list font project or file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font project or file",
        default=None,
        type=str)


    args = parser.parse_args()

    pass_precheck = True
    if not exists(args.input):
        pass_precheck = False
        print("input path not found: %s" % (args.input))

    if not exists(args.remove):
        pass_precheck = False
        print("remove path not found: %s" % (args.remove))

    if pass_precheck:
        font_delete_font_main(args)

if __name__ == "__main__":
    cli()
