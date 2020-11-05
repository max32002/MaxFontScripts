#!/usr/bin/env python3
#encoding=utf-8

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

import glob

def scan_folders(target_path):
    #path="."
    print("Checking path:", target_path)

    idx=0
    convert_count=0

    filename_pattern = target_path + "/*.svg"
    for name in glob.glob(filename_pattern):
        idx+=1
        #print("convert filename:", name)
        is_convert = False

        drawing = svg2rlg(name)
        new_name = name.replace('.svg','.png')
        renderPM.drawToFile(drawing, new_name, fmt="PNG")
        convert_count+=1

    print("Finish!\nconvert file count:%d\n" % (convert_count))

if __name__ == '__main__':
    import sys
    argument_count = 2
    if len(sys.argv)==argument_count:
        target_path = sys.argv[1]
        scan_folders(target_path)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s project.sfdir" % (sys.argv[0]))

