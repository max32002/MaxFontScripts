#!/usr/bin/env python3
#encoding=utf-8

#execute command:
# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge ~/Documents/noto/convert/expand_stroke.py --input ~/Documents/noto/abc.sfdir --width 8 --weight bold

# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge

import argparse
import math

def expand(args):

    #stroke_width = 52
    stroke_width = 34
    stroke_width = 28
    
    
    # expand_direction is ["light" | "bold"]
    expand_direction = "light"
    expand_direction = "bold"

    # only use when "light" version.
    stroke_join_limit=6

    output_ff = args.output
    if output_ff is None:
        output_ff = args.input
    
    # basic settings.
    ff_tmp, stroke_width, expand_direction = args.input, args.width, args.expand_direction

    stroke_cap = args.stroke_cap
    stroke_join = args.stroke_join

    print("Open font:", ff_tmp)
    print("Output:", output_ff)
    print("stroke_width:", stroke_width)
    print("expand_direction:", expand_direction)
    print("stroke_cap:", stroke_cap)
    print("stroke_join:", stroke_join)
    myfont=fontforge.open(ff_tmp)
    myfont.selection.all()

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


    skip_list = []

    idx = 0

    for glyph in myfont.selection.byGlyphs:
        idx +=1
        #unicode_string = str(hex(glyph.unicode))[2:]
        unicode_int = glyph.unicode
        if unicode_int in skip_list:
            continue

        if unicode_int <= 0:
            continue

    convert_count = 0
    for glyph in myfont.selection.byGlyphs:
        idx +=1
        #unicode_string = str(hex(glyph.unicode))[2:]
        
        # altuni, cause glyph expand stroke more times.
        if glyph.changed:
            continue

        unicode_int = glyph.unicode
        if unicode_int in skip_list:
            continue

        if unicode_int <= 0:
            continue
        
        #print("Process (%d): %s - %s" % (idx, char, unicode_string))
        #print("index:%d, unicode:%d , char:%s" % (idx,unicode_int,chr(unicode_int)))
        #print("altuni", glyph.altuni)
        #print("changed", glyph.changed)
        
        #default for thin expand stroke
        if expand_direction == "bold":
            # better version
            glyph.stroke("circular",stroke_width,cap=stroke_cap,join=stroke_join,angle=math.radians(45),removeinternal=True,simplify=True,removeoverlap="contour")
            convert_count += 1
            # stable version
            #glyph.stroke("circular",stroke_width,cap=stroke_cap,join=stroke_join,removeinternal=True,simplify=True)
        else:
            # "light"
            # better version
            glyph.stroke("circular",stroke_width,cap=stroke_cap,join=stroke_join,angle=math.radians(45),removeexternal=True,simplify=True,joinlimit=stroke_join_limit,removeoverlap="contour")
            convert_count += 1
            # stable version, for interrupe glyphs.
            #glyph.stroke("circular",stroke_width,cap=stroke_cap,join=stroke_join,removeexternal=True,simplify=True)
        #glyph.export("U%s.svg" % (unicode_string))


        if convert_count % 100 == 0:
            print("Processing index:%d (count:%d)" % (idx,convert_count))

    print("Done, total:%d, convert count:%d" % (idx, convert_count))
    myfont.save(output_ff)


def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--width",
        help="stroke_width",
        required=True,
        type=int)

    parser.add_argument("--expand_direction",
        help="expand direction",
        type=str)

    parser.add_argument("--output",
        help="output sfdir path",
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


    parser.add_argument("--stroke_cap",
        help="Expand Stroke Line Cap",
        default='round',
        type=str)

    parser.add_argument("--stroke_join",
        help="Expand Stroke Line Join",
        default='miter',
        type=str)

    args = parser.parse_args()

    expand(args)


if __name__ == "__main__":
    cli()
