#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import exists, normpath, basename
import argparse

def clear_main(args):
    target_string = args.string
    ff_path = args.input
    out_path = args.output
    skip_alt=False
    if args.skip_alt:
        skip_alt=True

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

    print("Open font:", ff_path)
    print("Save font:", out_path)

    if len(target_string) == 0:
        # is need read from file.
        string_file = args.file
        if len(string_file) > 0:
            if exists(string_file):
                my_list = []
                f = open(string_file,"r", encoding='utf-8')
                file_raw_list = f.readlines()
                for line in file_raw_list:
                    line = line.strip()
                    for char in line:
                        if len(char) > 0:
                            my_list.append(char)
                f.close()
                target_string = ''.join(my_list)
                print("string length in file:", len(target_string))
            else:
                print("input file not exist:", string_file)

    print("Selected char length:", len(target_string))

    if exists(ff_path):
        myfont=fontforge.open(ff_path)
        myfont, cleared_char_list = clear_glyph(myfont, target_string, skip_alt)
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

def clear_glyph(myfont, selected_chars, skip_alt=False):
    myfont.selection.all()
    all_glyph_list = list(myfont.selection.byGlyphs)
    print("Source font total glyph:", len(all_glyph_list))
    clear_char_list = set()
    idx = 0
    for glyph in all_glyph_list:
        idx +=1
        unicode_int = glyph.unicode
        if unicode_int <= 0:
            continue
        if glyph.width <= 0:
            continue
        debug = False       # online
        #debug = True
        if debug:
            print("-"*20)
            print("glyph originalgid:", glyph.originalgid)
            print("glyph unicode:", unicode_int)
            print("glyph altuni:", glyph.altuni)
            print("glyph char:", chr(unicode_int))
        if chr(unicode_int) in selected_chars:
            # to avoid: Lookup subtable contains unused glyph uni???? making the whole subtable invalid
            delete_flag = True
            if skip_alt:
                if not glyph.altuni is None:
                    delete_flag = False
            if delete_flag:
                glyph.clear()
                clear_char_list.add(unicode_int)
        if idx % 1000 == 0:
            print("Processing glyph: %d" % (idx))
    return myfont, clear_char_list


def cli():
    parser = argparse.ArgumentParser(
            description="clear glyph from font")

    parser.add_argument("--input",
        help="input font project or file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font project or file",
        default=None,
        type=str)

    parser.add_argument("--string",
        help="selected string",
        default='',
        type=str)

    parser.add_argument("--file",
        help="selected string file",
        default='',
        type=str)

    parser.add_argument("--skip_alt",
        help="let all alt char alive",
        action='store_true')

    args = parser.parse_args()

    pass_precheck = True
    if pass_precheck:
        clear_main(args)

if __name__ == "__main__":
    cli()
