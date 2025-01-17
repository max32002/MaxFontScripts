#!/usr/bin/env python3
#encoding=utf-8

import os
from os import listdir, remove
from os.path import join
import concurrent.futures

def load_unicode_from_file(filename_input, unicode_field):
    mycode = 0
    width_int = 0

    #print("filename_input", filename_input)
    myfile = open(filename_input, 'r')

    glyph_info = {}

    left_part_Encoding = 'Encoding: '
    left_part_Encoding_length = len(left_part_Encoding)

    left_part_Width = 'Width: '
    left_part_Width_length = len(left_part_Width)

    left_part_AltUni2 = 'AltUni2: '
    left_part_AltUni2_length = len(left_part_AltUni2)

    left_part_SplineSet = 'SplineSet'
    left_part_SplineSet_length = len(left_part_SplineSet)


    for x_line in myfile:
        #print(x_line)
        if left_part_Encoding == x_line[:left_part_Encoding_length]:
            right_part = x_line[left_part_Encoding_length:]
            glyph_info['encoding_raw']=right_part
            if ' ' in right_part:
                mychar_array = right_part.split(' ')
                if len(mychar_array) > 0:
                    mycode = int(mychar_array[unicode_field-1])
                    #print("bingo")
                    #break

        if left_part_Width == x_line[:left_part_Width_length]:
            right_part = x_line[left_part_Width_length:].strip()
            glyph_info['width_raw']=right_part
            width_int = int(float(right_part))

        if left_part_AltUni2 == x_line[:left_part_AltUni2_length]:
            right_part = x_line[left_part_AltUni2_length:].strip()
            glyph_info['altuni2_raw']=right_part
            if "." in right_part:
                glyph_info['altuni2']=right_part.split(".")[0]

        # Time to exit.
        if left_part_SplineSet == x_line[:left_part_SplineSet_length]:
            break
        
    myfile.close()
    myfile = None

    glyph_info['filepath']=filename_input
    glyph_info['unicode']=mycode
    glyph_info['width']=width_int

    return glyph_info


def load_files_to_set_dict(ff_folder, unicode_field, check_altuni2=False):
    my_set = set()
    my_dict = {}

    # 取得所有檔案與子目錄名稱
    file_paths = [os.path.join(ff_folder, file) for file in os.listdir(ff_folder) if file.endswith('.glyph') and os.path.isfile(os.path.join(ff_folder, file))]

    # multi thread
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(load_unicode_from_file, file_paths, [unicode_field] * len(file_paths))

    for glyph_info in results:
        unicode_info = 0
        if 'unicode' in glyph_info:
            unicode_info = glyph_info['unicode']

        if check_altuni2:
            if 'altuni2' in glyph_info:
                altuni2_info = glyph_info['altuni2']
                #print("altuni2_info:", altuni2_info)
                if len(altuni2_info) > 0:
                    altuni2_int = int(altuni2_info,16)
                    #print("altuni2_int:", altuni2_int)
                    my_set.add(altuni2_int)
                    my_dict[altuni2_int] = f

        #print('code:', unicode_info)
        if unicode_info > 0 and unicode_info < 0x110000:
            #print('code:', unicode_info)
            my_set.add(unicode_info)
            file_name = os.path.basename(glyph_info["filepath"])
            my_dict[unicode_info] = file_name
            #break

    # single thread
    '''
    for f in files:
        # must match extension only, exclude ".extension.tmp" file.
        extension = splitext(f)
        #print("extension:", extension[1])
        #break

        if extension[1] == '.glyph':
            #print('filename:', f)
            glyph_info = load_unicode_from_file(join(ff_folder,f), unicode_field)
            unicode_info = 0
            if 'unicode' in glyph_info:
                unicode_info = glyph_info['unicode']

            if check_altuni2:
                if 'altuni2' in glyph_info:
                    altuni2_info = glyph_info['altuni2']
                    #print("altuni2_info:", altuni2_info)
                    if len(altuni2_info) > 0:
                        altuni2_int = int(altuni2_info,16)
                        #print("altuni2_int:", altuni2_int)
                        my_set.add(altuni2_int)
                        my_dict[altuni2_int] = f

            if unicode_info > 0 and unicode_info < 0x110000:
                #print('code:', unicode_info)
                my_set.add(unicode_info)
                my_dict[unicode_info] = f    
    '''

    return my_set, my_dict
