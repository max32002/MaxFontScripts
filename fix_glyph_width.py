#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename, mkdir
from os.path import join, exists, normpath, basename, splitext

# to copy file.
import shutil

def update_width_from_file(file_path, unicode_field, target_width_int_min, target_width_int_max, new_width, is_read_only):
    output_filepath = file_path + ".tmp"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_Encoding = 'Encoding: '
    left_part_Encoding_length = len(left_part_Encoding)

    left_part_Width = 'Width: '
    left_part_Width_length = len(left_part_Width)

    is_found_target = False
    mycode = 0
    
    x_line = input_file.readline()
    #for x_line in input_file:
    target_width_int = int(float(target_width))
    while x_line:
        #print(x_line)
        new_line = x_line

        if left_part_Encoding == x_line[:left_part_Encoding_length]:
            right_part = x_line[left_part_Encoding_length:]
            if ' ' in right_part:
                mychar_array = right_part.split(' ')
                if len(mychar_array) > 0:
                    mycode = int(mychar_array[unicode_field-1])

        if left_part_Width == x_line[:left_part_Width_length]:
            right_part = x_line[left_part_Width_length:].strip()
            if right_part != target_width:
                value_in_file = int(float(right_part))

                if value_in_file >= target_width_int_min and value_in_file <= target_width_int_max:
                    if mycode > 0:
                        print("%s: Width:%s, file:%s" %(chr(mycode), right_part, file_path))
                        is_found_target = True
                        new_line = "%s%s\n" % (left_part_Width,target_width)

        output_file.write(new_line)
        x_line = input_file.readline()

    input_file.close()
    output_file.close()

    
    # for debug purpose
    if is_read_only:
        is_found_target = False 

    if is_found_target:
        is_copy_file_to_folder = True   # copy out the files by FontForge.
        is_copy_file_to_folder = False  # direct modify.

        if not is_copy_file_to_folder:
            remove(file_path)
            rename(output_filepath, file_path)
        else:
            # copy not fit glyph to fix.sfdir
            fix_folder = "fix.sfdir"
            if not exists(fix_folder):
                mkdir(fix_folder)
            else:
                pass

            source_path = file_path
            target_path = join(fix_folder, (basename(normpath(file_path))))
            shutil.copy(source_path,target_path)
    else:
        remove(output_filepath)


    return is_found_target

def scan_folder(ff_folder, unicode_field, target_width_int_min, target_width_int_max, new_width, is_read_only):
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

            # filter normal case
            if "uni" in f:
                #continue
                pass
                
            target_path = join(ff_folder,f)

            update_resulte = update_width_from_file(target_path, unicode_field, target_width_int_min, target_width_int_max, new_width, is_read_only)

            
            if update_resulte:
                match_count += 1
    print("file count:", file_count)
    print("update count:", match_count)


if __name__ == '__main__':
    #source_ff = 'Bakudai-Regular.sfdir'
    
    # from 1 to 3.
    #unicode_field = 2       # for Noto Sans
    unicode_field = 2
    
    accurate_percent = 0.22     # loss compare
    accurate_percent = 0.13     # tight compare
    accurate_percent = 0.05     # tight compare
    accurate_percent = 0.03     # tight compare
    accurate_percent = 0.01     # tight compare
    #accurate_percent = 0        # must match

    is_read_only = True         # for debug
    is_read_only = False        # online

    new_width = 1000

    import sys
    argument_count = 3
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        source_ff = source_ff.strip()

        target_width = sys.argv[2]
        target_width = target_width.strip()
        
        if len(source_ff) > 0 and len(target_width) > 0:

            target_width_int = int(target_width)
            target_width_int_min = target_width_int - (target_width_int * accurate_percent)
            target_width_int_max = target_width_int + (target_width_int * accurate_percent)
            print("target_width:", target_width)
            print("target_width_int_min:", target_width_int_min)
            print("target_width_int_max:", target_width_int_max)
            print("replace as new width:", new_width)

            if not exists(source_ff):
                if not ".sfdir" in source_ff:
                    source_ff += ".sfdir"
    
            if exists(source_ff):
                scan_folder(source_ff, unicode_field, target_width_int_min, target_width_int_max, new_width, is_read_only)
            
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name target_width" % (sys.argv[0]))
