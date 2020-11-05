#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename
from os.path import join, isdir, isfile

# common functions.
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def overwrite_config_file(file_path, new_version_string):
    output_filepath = file_path + ".tmp"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part_version = 'Version: '
    left_part_version_length = len(left_part_version)
    left_part_lang = 'LangName: '
    left_part_lang_length = len(left_part_lang)

    left_part_fontname = 'FontName:'
    left_part_fontname_length = len(left_part_fontname)
    left_part_fullname = 'FullName:'
    left_part_fullname_length = len(left_part_fullname)
    left_part_weight = 'Weight: '
    left_part_weight_length = len(left_part_weight)

    new_weight = ""
    if '-' in file_path:
        file_path_array = file_path.split("-")
        last_item = file_path_array[len(file_path_array)-1]

        my_delimitor_symbol = u'.sfdir'
        if my_delimitor_symbol in last_item:
            my_delimitor_index = last_item.find(my_delimitor_symbol)
            if my_delimitor_index >=0:
                new_weight = last_item[:my_delimitor_index]
    print("Weight:", new_weight)

    left_part_ttfweight = 'TTFWeight: '
    left_part_ttfweight_length = len(left_part_ttfweight)

    if not("-" in file_path and ".sfdir" in file_path):
        print("Error: must match weight in folder name, ex: fontname-Regular.sfdir")
        return
    
    old_weight = None

    for x_line in input_file:
        #print(x_line)
        new_line = x_line

        # chage font name
        if left_part_fontname == x_line[:left_part_fontname_length]:
            
            if "-" in new_line:
                old_weight = new_line.split('-')[1].strip()
                print('weight in config:"%s"' % (old_weight))

            if not old_weight is None:
                print('weight change to:"%s"' % (new_weight))
                new_line = new_line.replace('-'+old_weight,'-'+new_weight)

        # change fullname
        if left_part_fullname == x_line[:left_part_fullname_length]:
            if not old_weight is None:
                new_line = new_line.replace('-'+old_weight,'-'+new_weight)

        # chagne weight
        if left_part_weight == x_line[:left_part_weight_length]:
            new_line = left_part_weight + new_weight + "\n"
            if new_weight == "ExtraLight":
                new_line = left_part_weight + "Extra-Light\n"
            if new_weight == "Semi-Bold":
                new_line = left_part_weight + "Semi-Light\n"
            if new_weight == "Extra-Bold":
                new_line = left_part_weight + "Extra-Bold\n"

        # chage ttfweight
        if left_part_ttfweight == x_line[:left_part_ttfweight_length]:
            if new_weight == "ExtraLight" or new_weight == "Extra-Light":
                new_line = left_part_ttfweight + "200\n"
            if new_weight == "Light":
                new_line = left_part_ttfweight + "300\n"
            if new_weight == "Regular":
                new_line = left_part_ttfweight + "400\n"
            if new_weight == "Medium":
                new_line = left_part_ttfweight + "500\n"
            if new_weight == "SemiBold" or new_weight == "Semi-Bold":
                new_line = left_part_ttfweight + "600\n"
            if new_weight == "Bold":
                new_line = left_part_ttfweight + "700\n"
            if new_weight == "ExtraBold" or new_weight == "Extra-Bold":
                new_line = left_part_ttfweight + "800\n"
            if new_weight == "Black"or new_weight == "Heavy":
                new_line = left_part_ttfweight + "900\n"

        # chage version
        if left_part_version == x_line[:left_part_version_length]:
            new_line = left_part_version + new_version_string + "\n"

        # change version in lang
        if left_part_lang == x_line[:left_part_lang_length]:
            lang_version_string = "Version "
            if lang_version_string in x_line:
                mychar_array = x_line.split(lang_version_string)
                if len(mychar_array) > 0:
                    new_line = mychar_array[0] + lang_version_string + new_version_string
                    version_right_part = mychar_array[1]

                    my_delimitor_symbol = u'"'
                    if my_delimitor_symbol in version_right_part:
                        my_delimitor_index = version_right_part.find(my_delimitor_symbol)
                        my_delimitor_right_part = version_right_part[my_delimitor_index+len(my_delimitor_symbol):]
                        new_line += my_delimitor_symbol + my_delimitor_right_part

            if not old_weight is None:
                new_line = new_line.replace('-'+old_weight,'-'+new_weight)
                new_line = new_line.replace('"'+old_weight+'"','"'+new_weight+'"')

        output_file.write(new_line)

    input_file.close()
    output_file.close()

    remove(file_path)
    rename(output_filepath, file_path)

def scan_folders(new_version_string, prefix_string):
    # 指定要列出所有檔案的目錄
    folders = listdir(".")
    folders_count = 0
    for item in folders:
        if ".sfdir" in item and isdir(item) and prefix_string in item:
            folders_count += 1
            target_path = join(item,"font.props")
            if isfile(target_path):
                print("open config:", target_path)
                overwrite_config_file(target_path, new_version_string)
    print("match folders count:", folders_count)

if __name__ == '__main__':
    #prefix_string = "Baku"

    import sys
    argument_count = 3
    if len(sys.argv)==argument_count:
        new_version_string = sys.argv[1]
        prefix_string = sys.argv[2]
        scan_folders(new_version_string, prefix_string)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s 1.01 FontProjectPreix" % (sys.argv[0]))


