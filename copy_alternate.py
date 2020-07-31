#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import listdir, remove, rename
from os.path import join, exists

import json

# to copy/move file.
import shutil

def open_db(dictionary_filename):
    dict_data = None
    with open(dictionary_filename, 'r') as read_file:
        dict_data = json.load(read_file)
        read_file.close()

    return dict_data

def overwrite_config_encoding(file_path, new_encoding_string, unicode_field):
    output_filepath = file_path + ".tmp"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part = 'Encoding: '
    left_part_length = len(left_part)

    for x_line in input_file:
        #print(x_line)
        new_line = x_line

        if left_part == x_line[:left_part_length]:
            right_part = x_line[left_part_length:]
            if ' ' in right_part:
                mychar_array = right_part.split(' ')
                if len(mychar_array) > 0:
                    mychar_array[unicode_field-1]=str(new_encoding_string)
                    new_line = left_part + ' '.join(mychar_array)
        output_file.write(new_line)

    input_file.close()
    output_file.close()

    remove(file_path)
    rename(output_filepath, file_path)


def compare_dictionary(source_ff, unicode_field, full_dict):
    is_read_only = True     # debug
    #is_read_only = False    # online

    target_unicode_set, target_dict = LibGlyph.load_files_to_set_dict(source_ff, unicode_field)

    alternate_set = set()
    alternate_dict = {}
    for char_key in full_dict:
        char_dict = full_dict[char_key]
        for alternate in char_dict['alternate']:
            unicode_int = ord(alternate)
            alternate_set.add(unicode_int)
            alternate_dict[unicode_int] = ord(char_key)
    print("all alternate length:", len(alternate_set))

    diff_set_common =  target_unicode_set & alternate_set
    print("length more:", len(diff_set_common))

    copy_count = 0
    for item in diff_set_common:
        if not alternate_dict[item] in target_unicode_set:
            target_filename = "uni%s.glyph" % str(hex(alternate_dict[item]))[2:].upper()
            source_path = join(source_ff,target_dict[item])
            target_path = join(source_ff,target_filename)
            print("source char:%s to char:%s" % (chr(item),chr(alternate_dict[item])) )
            
            if not is_read_only:
                shutil.copy(source_path,target_path)
                overwrite_config_encoding(target_path, alternate_dict[item], unicode_field)
            
            # reset unicode
            copy_count += 1


    print("copy_count:", copy_count)


if __name__ == '__main__':
    #source_ff = 'Bakudai-Regular.sfdir'

    ctext_path = "/Users/chunyuyao/Documents/git/chinese_dictionary/Dictionary_lite.json"
    full_dict = open_db(ctext_path)

    # from 1 to 3.
    unicode_field = 1       # default
    unicode_field = 2       # for Noto Sans

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
                compare_dictionary(source_ff, unicode_field, full_dict)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))
