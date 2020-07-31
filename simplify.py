#!/usr/bin/env python3
#encoding=utf-8

#execute command:
# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge ~/Documents/noto/convert/simplify.py --input ~/Documents/noto/abc.sfdir --output xyz.sfdir

# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge

import argparse
import math

def simplify(args):

    output_ff = args.output
    if output_ff is None:
        output_ff = args.input
    
    # basic settings.
    ff_tmp = args.input

    print("Open font:", ff_tmp)
    print("Save to:", output_ff)
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
        

        '''
glyph.simplify([error_bound, flags, tan_bounds, linefixup, linelenmax])
Tries to remove excess points in the glyph if doing so will not perturb the curve by more than error-bound. Flags is a tuple of the following strings

ignoreslopes
Allow slopes to change

ignoreextrema
Allow removal of extrema

smoothcurves
Allow curve smoothing

choosehv
Snap to horizontal or vertical

forcelines
flatten bumps on lines

nearlyhvlines
Make nearly horizontal/vertical lines be so

mergelines
Merge adjacent lines into one

setstarttoextremum
Rotate the point list so that the start point is on an extremum

removesingletonpoints
If the contour contains just one point then remove it
        '''
        glyph.simplify()
        convert_count += 1


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


    args = parser.parse_args()

    simplify(args)


if __name__ == "__main__":
    cli()
