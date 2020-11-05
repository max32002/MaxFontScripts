#!/usr/bin/env python3
#encoding=utf-8

#execute command:
# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge bmp.py--input Regular.sfdir --output folder

import os
from os import mkdir
from os.path import exists
import argparse

# for read bmp.
from PIL import Image

def resize(filename, width):
    ret = False
    #im = Image.open( "U_36935.bmp" )
    im = Image.open( filename )
    #print(im.format, im.size, im.mode)
    #width = 1000
    ratio = float(width)/im.size[0]
    height = int(im.size[1]*ratio)
    # Image resizing methods resize() and thumbnail() take a resample argument, 
    # which tells which filter should be used for resampling. 
    # Possible values are: 
    # PIL.Image.NEAREST, PIL.Image.BILINEAR, PIL.Image.BICUBIC and PIL.Image.ANTIALIAS. 
    # Almost all of them were changed in this version.
    if im.size[0] != width:
        nim = im.resize( (width, height), Image.ANTIALIAS )
        #print(nim.size)
        #nim.save( "resized.jpg" )
        nim.save(filename)
        ret = True

    return ret

def export(ff_tmp, out_path, export_format, pixelsize, force_overwrite=True):
    print("Open font:", ff_tmp)
    print("Save dir:", out_path)
    print("Save format:", export_format)

    if not exists(out_path):
        mkdir(out_path)
    else:
        pass

    myfont=fontforge.open(ff_tmp)
    myfont.selection.all()

    idx = 0

    skip_list = []

    # read chars list from text.
    #for char in mychars:
        #myfont.selection.select(ord(char))

    export_counter = 0
    for glyph in myfont.selection.byGlyphs:
        idx +=1

        #unicode_string = str(hex(glyph.unicode))[2:]
        unicode_int = glyph.unicode
        if unicode_int in skip_list:
            continue

        if unicode_int <= 0:
            continue

        #if glyph.width >= 990:
            #continue

        if glyph.width <= 0:
            continue

        # continue from interrupe.
        #if idx <= 38500:
            #continue

        #filename="U_%d.svg" % (unicode_int)

        # due to the file count too large.
        profix_folder = str(unicode_int)[:1]
        target_folder = os.path.join(out_path,profix_folder)
        if not exists(target_folder):
            mkdir(target_folder)
        else:
            pass

        filename="U_%d.%s" % (unicode_int,export_format)
        target_path = os.path.join(target_folder,filename)

        export_flag = True

        if not force_overwrite:
            # some file is lost.
            if exists(target_path):
                
                # PS: OSError: image file is truncated (0 bytes not processed)
                # some file maybe broken, and filesize is undert 4K.
                # if exist file less then 4K, re-generate again.
                if os.path.getsize(target_path) > 4096:
                    # skip export.
                    export_flag = False

        if export_flag:
            if export_format in ['bmp','png']:
                glyph.export(target_path,pixelsize=pixelsize,bitdepth=1)
            else:
                glyph.export(target_path)
            export_counter += 1
            #glyph.export(filename)
            #glyph.export(filename,usetransform=True)
            #glyph.export(filename,usesystem=True)
            #break
            #print("width:",glyph.width)

            is_convert = False
            # resize Chinese Word only.
            # 歐文的字，可能會故意出血到畫框以外。
            if glyph.width >= 960:
                is_convert = resize(target_path,glyph.width)

        if idx % 1000 == 0:
            print("Processing (%d)export: %d" % (idx, export_counter))

    print("Done, total:%d" % (export_counter))


def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input",
        help="input font file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default=".",
        type=str)

    parser.add_argument("--format",
        help="export file format",
        default='bmp',
        type=str)

    parser.add_argument("--pixelsize",
        help="pixelsize",
        default=1000,
        type=int)

    # default is not overwrite, so run twice is okey.
    parser.add_argument("--overwrite",
        help="force overwrite",
        default="False",
        type=str)

    args = parser.parse_args()

    # default not overwrite.
    force_overwrite = False
    if args.overwrite == "True":
        force_overwrite = True

    export(args.input, args.output, args.format, args.pixelsize, force_overwrite=force_overwrite)

if __name__ == "__main__":
    cli()
