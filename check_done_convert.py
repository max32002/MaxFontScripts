#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import join, exists
import glob

import TtfConfig

# to copy/move file.
import shutil

def convert(path, config):
    idx=0
    convert_count=0

    filename_pattern = path + "/*.glyph"
    for name in glob.glob(filename_pattern):
        idx+=1
        print(idx,":convert filename:", name)

        source_path = name
        target_path = join("../undo",name)
        shutil.copy(source_path,target_path)

        if idx >= 100:
            break

    return idx

def scan_folders(target_path):
    #path="."
    print("Checking path:", target_path)
    file_count = 0
    file_count = convert(target_path, TtfConfig.TtfConfig())
    print("Finish!\ncheck file count:%d\n" % (file_count))

if __name__ == '__main__':
    import sys
    argument_count = 2
    if len(sys.argv)==argument_count:
        target_path = sys.argv[1]
        scan_folders(target_path)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s project.sfdir" % (sys.argv[0]))


