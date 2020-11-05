#!/usr/bin/env python3
#encoding=utf-8

from os import remove, rename
from os.path import join, isdir, isfile

def overwrite_text_file(file_path, old_string, new_string):
    output_filepath = file_path + ".tmp.python3"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    for x_line in input_file:
        new_line = x_line

        if old_string in x_line:
            new_line = new_line.replace(old_string,new_string)

        output_file.write(new_line)
    input_file.close()
    output_file.close()
    remove(file_path)
    rename(output_filepath, file_path)

if __name__ == '__main__':
    import sys
    argument_count = 4
    if len(sys.argv)==argument_count:
        target_path = sys.argv[1]
        old_string =  sys.argv[2]
        new_string =  sys.argv[3]
        if isfile(target_path):
            print("open text file:", target_path)
            print("Old String:", old_string)
            print("New String:", new_string)
            overwrite_text_file(target_path, old_string, new_string)
        else:
            print("path not exist:", target_path)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s project.sfdir \"old_string\" \"new_string\"" % (sys.argv[0]))


