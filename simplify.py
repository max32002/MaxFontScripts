#!/usr/bin/env python3
#encoding=utf-8

import argparse
import math
from os.path import exists, normpath, basename

def simplify_glyph(myfont, args):
    all_glyph_list = list(myfont.selection.byGlyphs)
    print("Source font total glyph:", len(all_glyph_list))

    skip_list = []
    idx = 0
    convert_count = 0
    for glyph in all_glyph_list:
        idx +=1
        
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

    return myfont

def simplify(args):
    ff_path = args.input
    out_path = args.output
    
    # basic settings.
    ff_path = args.input

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

    myfont=fontforge.open(ff_path)
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

    myfont.simplify(args.error_bound, ('mergelines','ignoreslopes','setstarttoextremum'))

    if export_as_font:
        myfont.generate(out_path)
    else:
        if out_path is None:
            myfont.save()
        else:
            myfont.save(out_path)

def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        default="output.ttf",
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

    parser.add_argument('--error_bound', type=float, default=0.1)

    args = parser.parse_args()
    simplify(args)


if __name__ == "__main__":
    cli()
