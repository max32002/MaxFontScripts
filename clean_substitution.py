#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join

def overwrite_config_file(file_path, readonly):
    output_filepath = file_path + ".tmp"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_substitution = 'Substitution2:'
    left_part_substitution_length = len(left_part_substitution)

    for x_line in input_file:
        #print(x_line)
        new_line = x_line

        # match Substitution2 line.
        if left_part_substitution == x_line[:left_part_substitution_length]:
            print("match at file:", file_path)
            continue

        output_file.write(new_line)

    input_file.close()
    output_file.close()

    if not readonly:
        remove(file_path)
        rename(output_filepath, file_path)


def scan_files_from_folder(ff_folder, readonly):
    files = listdir(ff_folder)
    match_count = 0
    for f in files:
        if '.glyph' in f:
            # skip hidden files.
            if f[:1] == ".":
                continue
            
            target_path = join(ff_folder,f)
            overwrite_config_file(target_path, readonly)

def clean_ff(source_ff, readonly):
    #source_ff = 'Bakudai-Regular.sfdir'
    scan_files_from_folder(source_ff, readonly)

if __name__ == '__main__':
    #readonly = True     # for test
    readonly = False   # online

    import sys
    argument_count = 2
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        if len(source_ff) > 1:
            if not ".sfdir" in source_ff:
                source_ff += ".sfdir"
            clean_ff(source_ff, readonly)
            
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))

