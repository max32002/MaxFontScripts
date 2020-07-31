#!/usr/bin/env python3
#encoding=utf-8

#execute command:
# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge ~/Documents/noto/convert/save_as.py --input ~/Documents/noto/abc.ttf --output ~/Documents/noto/abc.sfdir

# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge

import argparse

def save_as(args):
    ff_tmp, out_path = args.input, args.output

    print("Open font:", ff_tmp)
    myfont=fontforge.open(ff_tmp)
    print("Save sfdir:", out_path)

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

    myfont.save(out_path)

def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font file",
        required=True,
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

    args = parser.parse_args()
    save_as(args)

if __name__ == "__main__":
    cli()
