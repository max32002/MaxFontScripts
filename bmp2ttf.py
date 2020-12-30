#!/usr/bin/env python3
#encoding=utf-8

'''
PURPOSE:
    generate a font file(ttf format) with bitmaps    
'''

import os

BMP_PATH = './bmp/'
SVG_PATH = './svg/'
FONT_PROJECT= './myfont.sfdir'
FONT_PATH= './myfont.ttf'

import fontforge
# new font.
#font = fontforge.font()
# open exist font.
print("Open font:", FONT_PROJECT)
font=fontforge.open(FONT_PROJECT)

# prepare environment
if not os.path.exists(BMP_PATH):
    # make dir.
    print('mkdir bmp folder')
    os.system('mkdir -p ' + BMP_PATH)

if not os.path.exists(SVG_PATH):
    # make dir.
    print('mkdir svg folder')
    os.system('mkdir -p ' + SVG_PATH)

print('bmp transform to svg...')

for filename in os.listdir(BMP_PATH):
    bmp_filepath = os.path.join(BMP_PATH, filename)
    svg_filename = filename.replace('.bmp','.svg')
    svg_filepath = os.path.join(SVG_PATH, svg_filename)
    command='potrace -s ' + bmp_filepath + ' -o ' + svg_filepath

    try:
        os.system(command)
    except Exception as e:
        print(e)

print('bmp transform to svg finished, move svg image to svg folder.')


print('generate fonts...')

for filename in os.listdir(SVG_PATH):
    svg = os.path.join(SVG_PATH, filename)
    try:
        #image filename example: "U_001234.svg"
        glyph = font.createChar(int('0x'+filename.split('.')[0][-4:], 16) ,filename.split('.')[0]) 
        
        # force overwrite, must clear before import.
        glyph.clear()
        # if .clear() clean too many infomation, use below code instead.
        #glyph.layers[0] = fontforge.layer()
        #glyph.layers[1] = fontforge.layer()

        glyph.importOutlines(svg)

        #glyph.correctDirection()
        glyph.simplify()
        glyph.round()

    except Exception as e:
        print(e)
    except Error as err:
        print(err)

# not necessary to save, save only for debug purpose.
#font.save(FONT_PROJECT)

font.generate(FONT_PATH)
font.close()

print('generate fonts finished.^_^y')
