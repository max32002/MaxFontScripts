#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import listdir, remove
from os.path import join, getsize, exists

def scan_files_from_folder(ff_folder, size_to_delete, readonly, unicode_field):
    files = listdir(ff_folder)
    match_count = 0
    file_count = 0
    for f in files:
        file_count += 1
        if '.glyph' in f:
            # skip hidden files.
            if f[:1] == ".":
                continue

            if f == "nonmarkingreturn.glyph":
                continue

            # filter normal case
            if "uni" in f:
                #continue
                pass
                
            target_path = join(ff_folder,f)

            glyph_info = LibGlyph.load_unicode_from_file(join(ff_folder,f), unicode_field)
            unicode_info = 0
            if 'unicode' in glyph_info:
                unicode_info = glyph_info['unicode']

            if unicode_info <= 127:
                # keep file.
                continue


            filesize = getsize(target_path)
            if filesize <= size_to_delete:
                match_count += 1
                print("path:%s, size:%d" % (f,filesize))
                if not readonly:
                    remove(target_path)
    print("file count:", file_count)
    print("remove count:", match_count)

def clean_empty(source_ff, readonly):
    size_to_delete = 120

    # from 1 to 3.
    unicode_field = 2
    scan_files_from_folder(source_ff, size_to_delete, readonly, unicode_field)

if __name__ == '__main__':
    #source_ff = 'Bakudai-Regular.sfdir'
    
    readonly = True     # for test
    readonly = False   # online

    import sys
    argument_count = 2
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        if len(source_ff) > 0:
            if not exists(source_ff):
                if not ".sfdir" in source_ff:
                    source_ff += ".sfdir"
    
            if exists(source_ff):
                clean_empty(source_ff, readonly)
            
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))
