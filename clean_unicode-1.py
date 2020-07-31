#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import listdir, remove
from os.path import join, exists, splitext

# to copy/move file.
import shutil

def scan_files_from_folder(ff_folder, backup_folder, readonly, unicode_field, clean_max_count):
    files = listdir(ff_folder)
    match_count = 0
    file_count = 0
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
            target_path = join(backup_folder,f)

            glyph_info = LibGlyph.load_unicode_from_file(source_path, unicode_field)
            unicode_info = 0
            if 'unicode' in glyph_info:
                unicode_info = glyph_info['unicode']

            if unicode_info < 0:
                match_count += 1
                if not readonly:
                    # lazy to keep file.
                    #shutil.move(source_path, target_path)
                    remove(source_path)
                else:
                    print("if not readonly, move file to:", target_path)
                
                if match_count >= clean_max_count:
                    break
    print("file count:", file_count)
    print("remove count:", match_count)


if __name__ == '__main__':
    #source_ff = 'Bakudai-Regular.sfdir'
    
    backup_folder = "unicode-1"
    
    # from 1 to 3.
    unicode_field = 1       # default
    unicode_field = 2       # for Noto Sans

    readonly = True     # for test
    readonly = False   # online

    import sys
    argument_count = 2

    clean_max_count = 99999
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        if len(source_ff) > 0:
            if not exists(source_ff):
                if not ".sfdir" in source_ff:
                    source_ff += ".sfdir"
            if exists(source_ff):
                scan_files_from_folder(source_ff, backup_folder, readonly, unicode_field, clean_max_count)
    else:
        if len(sys.argv)==argument_count+1:
            source_ff = sys.argv[1]
            clean_max_count_string = sys.argv[2]
            if len(source_ff) > 0 and len(clean_max_count_string) > 0:
                clean_max_count = int(clean_max_count_string)
                if not exists(source_ff):
                    if not ".sfdir" in source_ff:
                        source_ff += ".sfdir"
                if exists(source_ff):
                    scan_files_from_folder(source_ff, backup_folder, readonly, unicode_field, clean_max_count)
        else:
            print("Argument must be: %d" % (argument_count -1))
            print("Ex:%s folder_name" % (sys.argv[0]))
