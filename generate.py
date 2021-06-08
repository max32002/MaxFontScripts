#!/usr/bin/env python3
#encoding=utf-8

#execute command:
# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge ~/Documents/noto/convert/save_as.py --input ~/Documents/noto/abc.sfdir --output ~/Documents/noto/abc.ttf

# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge

import argparse
import math

def generate(args):
    ff_tmp, out_path = args.input, args.output

    if out_path is None:
        if ".sfdir" in ff_tmp:
            out_path = ff_tmp.replace(".sfdir",".ttf")
    if out_path is None:
        print("output path not able to genereate")
        return

    print("Open sfdir:", ff_tmp)
    myfont=fontforge.open(ff_tmp)
    print("Save font:", out_path)
    #myfont.generate(out_path,flags=('apple','round'))

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

    namelist = args.namelist

    if namelist=="":
        myfont.generate(out_path)
    else:
        myfont.generate(out_path, namelist='AGL For New Fonts')


def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="inpoutputut font file",
        #required=True,
        type=str)

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
        default="1",
        type=str)

    args = parser.parse_args()
    generate(args)

if __name__ == "__main__":
    cli()
