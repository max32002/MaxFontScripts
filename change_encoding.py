#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, exists

def overwrite_config_file(file_path, readonly):
    old_code = None
    new_code = None
    is_found_new_code = False

    output_filepath = file_path + ".tmp"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_encoding = 'Encoding: '
    left_part_encoding_length = len(left_part_encoding)

    for x_line in input_file:
        #print(x_line)
        new_line = x_line

        # match Encoding line.
        if left_part_encoding == x_line[:left_part_encoding_length]:
            if ' ' in new_line:
                #print("match at file:", file_path)
                new_line_array = new_line.split(' ')
                old_code = new_line_array[1]
                new_code = new_line_array[2]

                if not new_code is None:
                    if len(new_code) > 0:
                        if new_code != "-1":
                            is_found_new_code = True

            if is_found_new_code:
                my_delimitor_symbol = u' '
                if my_delimitor_symbol in x_line:
                    my_delimitor_index = x_line.find(my_delimitor_symbol)
                    if my_delimitor_index >=0:
                        #print("1:",my_delimitor_index)
                        my_delimitor_index = x_line.find(my_delimitor_symbol,my_delimitor_index+1)
                        if my_delimitor_index >=0:
                            #print("2:",my_delimitor_index)
                            new_line = left_part_encoding + new_code + x_line[my_delimitor_index:]
        output_file.write(new_line)

    input_file.close()
    output_file.close()

    if not readonly:
        remove(file_path)
        rename(output_filepath, file_path)

    return is_found_new_code


def scan_files_from_folder(ff_folder, readonly):
    files = listdir(ff_folder)
    
    match_count = 0
    is_match_in_file = False

    filename_ext = ".glyph"
    filename_ext_length = len(filename_ext)
    for f in files:
        if filename_ext == f[-1 * filename_ext_length:]:
            # skip hidden files.
            if f[:1] == ".":
                continue
            
            target_path = join(ff_folder,f)
            #print("target_path:", target_path)
            is_match_in_file = overwrite_config_file(target_path, readonly)

            if is_match_in_file:
                match_count += 1
            #break

    print("match file count:", match_count)

def change_encoding(source_ff, readonly):
    scan_files_from_folder(source_ff, readonly)

if __name__ == '__main__':
    #source_ff = 'Bakudai-Regular.sfdir'
    
    #readonly = True     # for test
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
                change_encoding(source_ff, readonly)
            
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:get_ttf_chars.py folder_name")
