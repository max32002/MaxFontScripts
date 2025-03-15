#!/usr/bin/env python3
#encoding=utf-8

import os
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
    print("Svg path:", args.svg_path)
    print("Filename pattern:", args.filename_pattern)
    print("Filename source:", args.filename_source)
    print("export_as_font:", export_as_font)

    if exists(ff_path):
        myfont=fontforge.open(ff_path)
        myfont, import_char_list = import_svg(myfont, args.svg_path, args.filename_pattern, args.filename_source, scale, simplify, args.width)

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

def import_svg(myfont, svg_path, filename_pattern, filename_source, scale, simplify, width):

    import_char_list = set()
    fail_char_list = set()

    # 獲取 SVG 檔案列表
    svg_files = [f for f in os.listdir(svg_path) if f.endswith(".svg")]

    idx = 0
    for filename in svg_files:
        idx += 1

        # 從檔名中提取 Unicode 值或字元
        if filename_source == 'unicode_int':
            try:
                unicode_int = int(filename.replace(".svg", ""))
            except ValueError:
                print(f"警告：無法從檔名 '{filename}' 中提取 Unicode 值。")
                continue
        elif filename_source == 'unicode_hex':
            try:
                unicode_int = int(filename.replace(".svg", ""), 16)
            except ValueError:
                print(f"警告：無法從檔名 '{filename}' 中提取十六進制 Unicode 值。")
                continue
        else: # filename_source == 'char'
            unicode_int = ord(filename.replace(".svg", ""))

        svg_filepath = os.path.join(svg_path, filename)

        debug = False
        #debug = True

        if debug:
            print("-" * 20)
            print("svg path:", svg_filepath)
            print("filename:", filename)
            print("unicode_int:", unicode_int)
            print("char:", chr(unicode_int))

        try:
            # 檢查字形是否存在
            myfont.selection.all()
            all_glyph_list = list(myfont.selection.byGlyphs)
            glyph_exists = False
            for glyph in all_glyph_list:
                if glyph.unicode == unicode_int:
                    existing_glyph = glyph
                    glyph_exists = True
                    break

            if glyph_exists:
                glyph = myfont[unicode_int]
                glyph.clear()
                glyph.importOutlines(svg_filepath, scale=scale, simplify=simplify)
                glyph.width = existing_glyph.width # 從現有字形讀取寬度
                import_char_list.add(glyph.originalgid)
            else:
                if debug:
                    print(f"嘗試新增字形：Unicode {unicode_int} ({chr(unicode_int)})，檔案：{svg_filepath}")
                myfont.createChar(unicode_int)
                glyph = myfont[unicode_int]
                glyph.importOutlines(svg_filepath, scale=scale, simplify=simplify)
                glyph.width = width # 從 args 中獲取寬度
                import_char_list.add(glyph.originalgid)
                if debug:
                    print(f"成功新增字形：Unicode {unicode_int} ({chr(unicode_int)})")

        except Exception as fontforge_exc:
            print(f"FontForge 錯誤：Unicode {unicode_int}，檔案：{svg_filepath}，錯誤訊息：{fontforge_exc}")
            fail_char_list.add(unicode_int)
            pass

        if idx % 1000 == 0:
            print("Processing glyph: %d" % (idx))

    print("Imported count:", len(import_char_list))
    if len(fail_char_list) > 0:
        print("Failed count:", len(fail_char_list))
        print("Failed char:", fail_char_list)

    return myfont, import_char_list


def cli():
    parser = argparse.ArgumentParser(
            description="import svg to font")

    parser.add_argument("--input",
        help="input font project or file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font project or file",
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

    parser.add_argument("--width",
                        help="字形寬度，預設值為 1000",
                        type=int,
                        default=1000)

    args = parser.parse_args()

    pass_precheck = True
    
    if not exists(args.svg_path):
        pass_precheck = False
        print("svg path not found: %s" % (args.svg_path))

    if pass_precheck:
        import_main(args)

if __name__ == "__main__":
    cli()
