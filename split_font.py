#!/usr/bin/env python3
# coding=utf8

import os
import argparse

# Up to Chrome 99, the max uncompressed size (e.g. ttf) of a font file is 30 MB.
# Please tune this value to split a font file to multiple files with size <= 30 MB.
#maxGlyphsPerFile = 15000

def splitFontFile(originalFile, max_glyphs, font_ext="ttf"):
    filename = os.path.basename(originalFile)
    filename = filename.split('.')[0]
    font = fontforge.open(originalFile)
    font.selection.all()
    glyphs = font.selection.byGlyphs
    totalGlyphs = len(list(glyphs))
    totalFiles = int(totalGlyphs / max_glyphs + 0.5)
    print(f'{originalFile} totalFiles: {totalFiles}')

    for f in range(totalFiles):
        g = 0
        gMin = f * max_glyphs
        gMax = (f + 1) * max_glyphs
        for glyph in glyphs:
            # Clear glyph out of range.
            if not(gMin <= g and g < gMax):
                glyph.clear()
            g = g + 1
        # Use this to check uncompressed font file sizes.
        #font.generate(f'{filename}-{f+1}.ttf')
        # Use this for compressed outputs.
        font.generate(f'{filename}-{f+1}.{font_ext}')
        font.close()
        font = fontforge.open(originalFile)
        font.selection.all()
        glyphs = font.selection.byGlyphs
    font.close()
    

def cli():
    parser = argparse.ArgumentParser(
            description="split font")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument('--max_glyphs', type=int, default=15000)

    parser.add_argument('--font_ext', type=str, default="ttf")
    

    args = parser.parse_args()

    pass_precheck = True
    
    if not os.path.exists(args.input):
        pass_precheck = False
        print("font file not found: %s" % (args.input))

    if pass_precheck:
        splitFontFile(args.input, args.max_glyphs, args.font_ext)

if __name__ == "__main__":
    cli()
