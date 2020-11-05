#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, exists, splitext

# to copy/move file.
import shutil

def contain_alt(file_path):
    ret = False

    input_file = open(file_path, 'r')

    left_part_alt = 'AltUni2: '
    left_part_alt_length = len(left_part_alt)

    left_part_SplineSet = 'SplineSet'
    left_part_SplineSet_length = len(left_part_SplineSet)

    x_line = input_file.readline()
    for x_line in input_file:
    #while x_line:
        #print(x_line)

        if left_part_alt == x_line[:left_part_alt_length]:
            ret = True
            break

        if left_part_SplineSet == x_line[:left_part_SplineSet_length]:
            break
        #x_line = input_file.readline()

    return ret


def scan_files(ff_folder, target_folder):
    files = listdir(ff_folder)
    file_count = 0
    copy_count = 0
    for f in files:
        file_count += 1

        # must match extension only, exclude ".extension.tmp" file.
        extension = splitext(f)
        #print("extension:", extension[1])
        #break

        if extension[1] == '.glyph':
            # skip hidden files.
            if f[:1] == ".":
                continue

            if f == "nonmarkingreturn.glyph":
                continue
                
            source_path = join(ff_folder,f)

            alt_check = contain_alt(source_path)
            if alt_check:
                #print("match filepath:", source_path)
                target_path = join(target_folder,f)
                shutil.copy(source_path,target_path)
                copy_count += 1
    print("file_count:", file_count)
    print("copy_count:", copy_count)


if __name__ == '__main__':

    import sys
    argument_count = 3

    clean_max_count = 99999
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        target_folder = sys.argv[2]
        if len(source_ff) > 0:
            if not exists(source_ff):
                if not ".sfdir" in source_ff:
                    source_ff += ".sfdir"
            if exists(source_ff):
                scan_files(source_ff,target_folder)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s ff_folder target_folder" % (sys.argv[0]))
