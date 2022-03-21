#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph
import GlyphCompare

from os import remove
from os.path import join, exists, abspath
from os import mkdir

# to copy file.
import shutil

import json
import argparse

import subprocess, sys

import glob


def load_config_files(import_file, skip_list_file, thin_component_filepath, heavy_component_filepath, skip_average_redical_filepath):
    target_chars_list = []
    if exists(import_file):
        f = open(import_file,"r")
        #solution #1, read all.
        #target_chars_list = f.readlines()

        #solution #2, read each line.
        file_raw_list = f.readlines()
        for line in file_raw_list:
            line = line.strip()

            if len(line) == 0:
                continue

            # default use compose command
            content_compose_commnad = True

            if content_compose_commnad:
                # line to long.
                if len(line) > 120:
                    content_compose_commnad = False
                # line too short.
                if len(line) == 1:
                    content_compose_commnad = False

            if content_compose_commnad:
                if not ' ' in line:
                    content_compose_commnad = False

            if content_compose_commnad:
                # compose command mode.
                target_chars_list.append(line)
            else:
                # raw data mode.
                for char in line:
                    if len(char) > 0:
                        target_chars_list.append(char)
        f.close()
    #target_chars_list = target_chars_raw.split('\n')

    skip_list = []
    if exists(skip_list_file):
        f = open(skip_list_file,"r")
        file_raw_list = f.readlines()
        for line in file_raw_list:
            line = line.strip()
            for char in line:
                if len(char) > 0:
                    skip_list.append(char)
        f.close()

    DEFAULT_THIN_COMPONENT = "大丿山古衤木片土爿干火扌羊丰忄于十目卜文申礻止日阝王力女亻牜彡冫⺪氵月自白巾弓言𧾷犭禾"
    # special case.
    DEFAULT_THIN_COMPONENT += "亢㚇戉番負賛壹害"
    
    DEFAULT_HEAVY_COMPONENT = "倉票畐丹念祭賴卵夾分翟芻瓜少宛肖羽兆卑八心"

    DEFAULT_SKIP_AVERAGE_MODE_REDICAL = '金糸魚'

    THIN_COMPONENT = []
    HEAVY_COMPONENT = []
    skip_average_mode_redical_list = []

    if exists(thin_component_filepath):
        f = open(thin_component_filepath,"r")
        file_raw_list = f.readlines()
        for line in file_raw_list:
            line = line.strip()
            for char in line:
                if len(char) > 0:
                    THIN_COMPONENT.append(char)
        f.close()
    if len(THIN_COMPONENT)==0:
        THIN_COMPONENT = DEFAULT_THIN_COMPONENT

    if exists(heavy_component_filepath):
        f = open(heavy_component_filepath,"r")
        file_raw_list = f.readlines()
        for line in file_raw_list:
            line = line.strip()
            for char in line:
                if len(char) > 0:
                    HEAVY_COMPONENT.append(char)
        f.close()

    if len(HEAVY_COMPONENT)==0:
        HEAVY_COMPONENT = DEFAULT_HEAVY_COMPONENT

    
    if exists(skip_average_redical_filepath):
        f = open(skip_average_redical_filepath,"r")
        file_raw_list = f.readlines()
        for line in file_raw_list:
            line = line.strip()
            for char in line:
                if len(char) > 0:
                    skip_average_mode_redical_list.append(char)
        f.close()

    if len(skip_average_mode_redical_list)==0:
        skip_average_mode_redical_list = DEFAULT_SKIP_AVERAGE_MODE_REDICAL



    return target_chars_list, skip_list, THIN_COMPONENT,HEAVY_COMPONENT,skip_average_mode_redical_list

def get_font_info(working_ff, UNICODE_FIELD):
    print("loading working .sfdir:", working_ff)
    ff_unicode_set, ff_dict = LibGlyph.load_files_to_set_dict(working_ff, UNICODE_FIELD)
    print("working font glyph length:", len(ff_unicode_set))

    # default value
    GLYPH_WIDTH, GLYPH_UNDERLINE = load_font_props(working_ff)
    print("GLYPH_WIDTH:", GLYPH_WIDTH)
    print("GLYPH_UNDERLINE:", GLYPH_UNDERLINE)

    return ff_unicode_set, ff_dict, GLYPH_WIDTH, GLYPH_UNDERLINE

def preview(target_ff):
    if not "/" in target_ff:
        target_ff = abspath(target_ff)
    cmd = "/Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge " + target_ff
    process = subprocess.Popen(cmd, shell=True)


def clean_target(path):
    filename_pattern = path + "/*.glyph"
    idx=0
    for name in glob.glob(filename_pattern):
        idx+=1
        remove(name)
    return idx

def load_font_props(working_ff):
    GLYPH_WIDTH, GLYPH_UNDERLINE = 1024, -200

    filename_input = join(working_ff, "font.props")
    myfile = open(filename_input, 'r')
    
    left_part_Ascent = 'Ascent:'
    left_part_Ascent_length = len(left_part_Ascent)
    left_part_Descent = 'Descent:'
    left_part_Descent_length = len(left_part_Descent)
    
    Ascent = GLYPH_WIDTH - GLYPH_UNDERLINE
    Descent = GLYPH_UNDERLINE * -1
    for x_line in myfile:
        if left_part_Descent == x_line[:left_part_Descent_length]:
            right_part = x_line[left_part_Descent_length:].strip()
            if len(right_part) > 0:
                Descent = int(float(right_part))

        if left_part_Ascent == x_line[:left_part_Ascent_length]:
            right_part = x_line[left_part_Ascent_length:].strip()
            if len(right_part) > 0:
                Ascent = int(float(right_part))

    GLYPH_UNDERLINE = Descent * -1
    GLYPH_WIDTH = Ascent + Descent

    myfile.close()

    return GLYPH_WIDTH, GLYPH_UNDERLINE


def open_db(dictionary_filepath):
    dict_data = None
    with open(dictionary_filepath, 'r') as read_file:
        dict_data = json.load(read_file)
        read_file.close()
    return dict_data

def save_db(dictionary_filepath,json_obj):
    # save to disk.
    json_string = json.dumps(json_obj)
    with open(dictionary_filepath, 'w') as outfile:
        outfile.write(json_string)
        outfile.close()

# only need run once at initial step.
def get_all_position(char_dict):
    # list all keys
    #print('dict_data.keys = ', dict_data.keys())
    all_position = []
    #print("length:", len(dict_data.keys()))
    for char in dict_data:
        #if char=='姚':
        if True:
            char_dict = dict_data[char]
            if 'component' in char_dict:
                component_dict = char_dict['component']

                for pos in component_dict:
                    if len(pos)>0:
                        #print("pos:", pos)
                        #if pos=="。 具有相關結構":
                        if pos=="and":
                            print("char:", char, ord(char), )

                        if not pos in all_position:
                            all_position.append(pos)
                #print("char:", char_dict)

    print("all_position:", all_position)

def get_position_key_by_name(all_position,key_name):
    ret = -1
    all_position_length = len(all_position)
    for pos_idx in range(all_position_length):
        pos_key = all_position[pos_idx]
        if pos_key == key_name:
            ret = pos_idx
            break
    return ret

# PS: no used for now.
def parse_position_dictionary(dict_data, all_position):
    pos_dict = {}

    all_position_length = len(all_position)
    for pos_idx in range(all_position_length):
        pos_key = all_position[pos_idx]
        
        # debug purpose
        #if not pos_key == "左":
            #continue

        pos_set = set()
        for char in dict_data:
            char_dict = dict_data[char]
            if 'component' in char_dict:
                component_dict = char_dict['component']
                if pos_key in component_dict:
                    pos_data = component_dict[pos_key]
                    if not pos_data in pos_set:
                        pos_set.add(pos_data)

        pos_dict[pos_key]=list(pos_set)

    #print("pos dict:", pos_dict)
    return pos_dict


def get_supported_position_set(dict_data, ff_unicode_set, all_position):
    supported_position_set = set()
    supported_position_dict = {}

    for ff_unicode in ff_unicode_set:
        char = chr(ff_unicode)
        # debug purpose
        #if not char == "經":
            #continue

        if char in dict_data:
            strokes_total = 0
            char_dict = dict_data[char]

            if 'strokes_total' in char_dict:
                strokes_total = char_dict['strokes_total']

            if 'component' in char_dict:
                component_dict = char_dict['component']
                for pos_key in component_dict:
                    pos_data = component_dict[pos_key]
                    pos_key_id = get_position_key_by_name(all_position, pos_key)
                    supported_position_key = "%d_%d" % (pos_key_id,ord(pos_data))
                    if not supported_position_key in supported_position_set:
                        supported_position_set.add(supported_position_key)
                        
                    if not supported_position_key in supported_position_dict:
                        supported_position_dict[supported_position_key]=[]
                    supported_position_dict[supported_position_key].append((char,strokes_total))


    #print("supported_position_set:", supported_position_set)
    return supported_position_set, supported_position_dict

def travel_preprocess(ff_unicode_set, dictionary_filepath):
    # hard code new, maybe change it in future.
    dict_data = open_db(dictionary_filepath)

    # cache the resule from json file.
    # only need run once.
    #all_position = get_all_position(dict_data)
    # exculde '具有相關結構', because no used.
    all_position = ['上', '下', '周圍', '中心', '左', '右', '左上', '右下', '左下', '右上', '左、右、上', '中間', '合併', '加', '上左下', '中和右', '左右', '中']
    
    #pos_dict_filepath = 'PosDict.json'

    #pos_dict = parse_position_dictionary(dict_data, all_position)
    # reponse time too soon, no need cache.
    #save_db(pos_dict_filepath, pos_dict)

    #print("compute supported_position_set...")
    supported_position_set, supported_position_dict = get_supported_position_set(dict_data, ff_unicode_set, all_position)

    return dict_data, all_position, supported_position_set, supported_position_dict

def get_skip_related_glyph_count(related_glyph_length):
    skip_to_index = -1
    import random
    if related_glyph_length >= 2:
        # match rich resource.
        if related_glyph_length >= 10:
            if related_glyph_length >= 30:
                # match very rich resource.
                # 後面筆畫太多的字，拆字常會出問題。
                skip_to_index = random.randint(0, 15)
            else:
                skip_to_index = random.randint(0, int(related_glyph_length * 0.3))
        else:
            skip_to_index = random.randint(0, int(related_glyph_length)-1)
        #print("skip_to_index:%d, full length:%d" % (skip_to_index, related_glyph_length))
        skip_to_index -= 1

    return skip_to_index

def merge_component(target_ff, char, char_info_array, combine_list, file_index, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, SHOW_DEBUG_MESSAGE, output_file, add_extra_finetune_commands):
    component_rule = combine_list[0][1] + combine_list[1][1]
    #print("match supported list:", char)
    #print("combin glyph list:", combine_list)
    output_folder = target_ff
    unicode_int = ord(char)

    char_commands_1 = []
    for cmd in char_info_array:
        if ":" in cmd:
            cmd_array = cmd.split(':')
            if "1" in cmd_array[1]:
                char_commands_1.append(cmd)

    char_commands_2 = []
    for cmd in char_info_array:
        if ":" in cmd:
            cmd_array = cmd.split(':')
            if "2" in cmd_array[1]:
                char_commands_2.append(cmd)

    is_component_rule_changed = False
    if combine_list[1][1] != combine_list[1][0]:
        is_component_rule_changed = True

    if is_component_rule_changed and add_extra_finetune_commands:
        #print("component_rule_changed, apply extra commands:")
        #print("char_commands_2 before:", char_commands_2)

        redical = combine_list[0][3]

        messsage = "component_rule:%s" % (component_rule)
        messsage += "redical:%s" % (redical)
        output_file.write(messsage + "\n")
        if SHOW_DEBUG_MESSAGE:
            print(messsage)

        is_apply_extra_command = False

        if component_rule=='左下右上':
            cmd="SCALE::XY:0.75"
            char_commands_2.append(cmd)
            is_apply_extra_command = True

            # default
            cmd="MOVE::X:" + str(int(GLYPH_WIDTH * 0.09))
            if redical in '走是鬼毛支虎風风':
                cmd="SCALE::XY:0.95"
                char_commands_2.append(cmd)
                cmd="MOVE::X:" + str(int(GLYPH_WIDTH * 0.2))

            if redical in '尢':
                cmd="SCALE::XY:0.95"
                char_commands_2.append(cmd)
                cmd="MOVE::X:" + str(int(GLYPH_WIDTH * 0.2))
            char_commands_2.append(cmd)

            cmd="MOVE::Y:" + str(int(GLYPH_WIDTH * 0.09))
            char_commands_2.append(cmd)

        if component_rule=='左上右下':
            cmd="SCALE::XY:0.8"
            char_commands_2.append(cmd)
            is_apply_extra_command = True
            
            cmd="MOVE::X:" + str(int(GLYPH_WIDTH * 0.09))
            char_commands_2.append(cmd)

            # default
            cmd="MOVE::Y:" + str(-1 * int(GLYPH_WIDTH * 0.09))
            if redical in '尸':
                cmd="SCALE::XY:0.9"
                char_commands_2.append(cmd)

                cmd="MOVE::Y:" + str(-1 * int(GLYPH_WIDTH * 0.10))

            if redical in '麻':
                cmd="SCALE::XY:0.75"
                char_commands_2.append(cmd)

                cmd="MOVE::Y:" + str(-1 * int(GLYPH_WIDTH * 0.20))
            char_commands_2.append(cmd)

        if is_apply_extra_command:
            print("char_commands_2 after:", char_commands_2)
            pass

    stroke_dict_1, unicode_int_1 = GlyphCompare.get_stroke_dict(combine_list[0][0], UNICODE_FIELD, char_commands_1)
    stroke_dict_2, unicode_int_2 = GlyphCompare.get_stroke_dict(combine_list[1][0], UNICODE_FIELD, char_commands_2)

    #print("component_rule, GLYPH_WIDTH, GLYPH_UNDERLINE:", component_rule, GLYPH_WIDTH, GLYPH_UNDERLINE)
    is_found_component, new_stroke_dict = GlyphCompare.merge_stroke(stroke_dict_1, stroke_dict_2, component_rule, GLYPH_WIDTH, GLYPH_UNDERLINE, add_extra_finetune_commands)

    if SHOW_DEBUG_MESSAGE:
        print("is_found_component:", is_found_component)

    glyph_filepath = None
    if is_found_component:
        glyph_filepath = GlyphCompare.new_glyph_file(output_folder, unicode_int, GLYPH_WIDTH, file_index=file_index)
        GlyphCompare.write_to_file(glyph_filepath, new_stroke_dict)
        print("(%d) char: %s , write_to_file: %s" % (file_index, char, glyph_filepath))
        
    return is_found_component, glyph_filepath

def pair_related_char(working_ff, target_ff, shake_redical, ff_dict, dict_data, pos_key, rule_name, pos_data, related_glyph_list, use_orginal_glyph_instead_of_component, combine_list, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, tmp_ff, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_DEBUG_MESSAGE, output_file):
    related_glyph_length = len(related_glyph_list)
    pair_result = False

    #extract_mode = 1    # compare two glyph to get intersection
    extract_mode = 2

    is_match_pre_require = False

    if extract_mode==1:
        if related_glyph_length >=2:
            is_match_pre_require = True

    if extract_mode==2:
        is_match_pre_require = True

    if is_match_pre_require:

        # 避免元件都長一樣。
        skip_to_index = -1
        if shake_redical == "True":
            skip_to_index = get_skip_related_glyph_count(related_glyph_length)

        if SHOW_DEBUG_MESSAGE:
            print("skip_to_index:", skip_to_index)

        for related_idx in range(related_glyph_length):
            if related_idx <= skip_to_index:
                continue

            related_char,strokes_total = related_glyph_list[related_idx]
            filename_1 = ff_dict[ord(related_char)]
            
            messsage = "related_char: %s (%s)" % (related_char,filename_1)
            output_file.write(messsage + "\n")
            if SHOW_DEBUG_MESSAGE:
                print(messsage)
            #print("%s:%s" % (related_char_next,filename_2))

            component = pos_data
            output_folder = target_ff
            filename_input_1 = join(working_ff,filename_1)

            # compare two to get intersection.
            if extract_mode==1 and related_glyph_length >1:
                related_char_next,strokes_total_next = related_glyph_list[(related_idx+1) % related_glyph_length]

                filename_2 = ff_dict[ord(related_char_next)]
                filename_input_2 = join(working_ff,filename_2)

                intersection_result, glyph_filepath = GlyphCompare.compare_intersection(component, filename_input_1, filename_input_2, UNICODE_FIELD, GLYPH_WIDTH, tmp_ff)
                messsage = "compare_intersection result:%s" % (str(intersection_result))
                output_file.write(messsage + "\n")
                if SHOW_DEBUG_MESSAGE:
                    print(messsage)
                if intersection_result:
                    pair_result = True
                    combine_list.append(glyph_filepath)
                    break

            # use rule_no.
            if extract_mode==2:
                parse_char = related_char

                # 使用非最佳解
                if use_orginal_glyph_instead_of_component:
                    rule_name = "全"

                # too many debug message. @_@; hard to find my target.
                SHOW_STROKE_DEBUG_MESSAGE = False
                #SHOW_STROKE_DEBUG_MESSAGE = True   # more detail debug message.
                intersection_result, glyph_filepath = GlyphCompare.component_from_rule(parse_char, dict_data, rule_name, component, filename_input_1, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, tmp_ff, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_STROKE_DEBUG_MESSAGE)

                messsage = "component_from_rule result:%s" % (str(intersection_result))
                output_file.write(messsage + "\n")
                if SHOW_DEBUG_MESSAGE:
                    print(messsage)
                if intersection_result:
                    pair_result = True
                    combine_list.append([glyph_filepath,pos_key,rule_name,component,related_char])
                    break
    return pair_result, combine_list

def get_related_glyph_list(supported_position_key,supported_position_set,supported_position_dict,skip_list):
    related_glyph_list = []
    if supported_position_key in supported_position_set:
        related_glyph_list = supported_position_dict[supported_position_key]
        related_glyph_list = sorted(related_glyph_list, key=lambda x: x[1])

        
        # due to current database some char use '簡體字筆畫' componet.
        #("skip_list:", skip_list)
        # 先刪除 skip list, 是為了套用 use_orginal_glyph_instead_of_component
        related_glyph_length = len(related_glyph_list)
        idx_offset = 0
        for related_idx in range(related_glyph_length):
            related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
            if related_char in skip_list:
                del related_glyph_list[related_idx - idx_offset]
                idx_offset += 1
    return related_glyph_list

def travel_glyph(target_ff, working_ff, tmp_ff, dict_data, target_chars_list, skip_list, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, ff_unicode_set, ff_dict, all_position, supported_position_set, supported_position_dict, shake_redical, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, SHOW_DEBUG_MESSAGE, log_filepath, add_extra_finetune_commands):
    output_file = open(log_filepath, 'w')

    total_lost_char_list = ""

    char_idx=-1
    file_index = 1
    for char_info in target_chars_list:
        char = ''
        
        # blank line.
        char_info = char_info.strip()
        if len(char_info) == 0:
            continue
        
        # too many messsage.
        #print("char_info:", char_info, len(char_info))

        char_info_array = []
        if ' ' in char_info:
            char_info_array = char_info.split(' ')
            char = char_info_array[0]
        else:
            char = char_info[:1]

        char_idx += 1

        if ord(char) in ff_unicode_set:
            #output_is_ready_message = True      # for debug.
            output_is_ready_message = False     # online

            if output_is_ready_message:
                output_file.write(('=' * 40) + '\n')
                messsage = "idx:%d char:%s is ready." % (char_idx, char)
                output_file.write(messsage + "\n")

                if SHOW_DEBUG_MESSAGE:
                    print(messsage)
        else:
            # queue the lost chars.
            total_lost_char_list += char

            output_file.write(('=' * 40) + '\n')
            messsage = "idx:%d char:%s (U+%s) is lost." % (char_idx, char,str(hex(ord(char)))[2:].upper())
            output_file.write(messsage + "\n")
            if SHOW_DEBUG_MESSAGE:
                print(messsage)

            is_match_supported_set = False
            combine_list = []
            if char in dict_data:
                char_dict = dict_data[char]
                if 'component' in char_dict:
                    component_dict = char_dict['component']

                    is_match_supported_set = True

                    compare_count = 0
                    for pos_key in component_dict:
                        # 因為暫時沒有參考價值
                        if pos_key=='具有相關結構':
                            continue

                        # for now, only these position able to handle.
                        # TODO: other positions.
                        # PS: 不要先取左邊，因為大多情況會「斜斜的」，大多情況左邊不會缺字，是缺右邊。
                        if not(pos_key in ['右','下','上','左下','右上','左','右下','左上']):
                            continue

                        # default use parent pos_key
                        rule_name = pos_key

                        compare_count += 1
                        pos_data = component_dict[pos_key]
                        pos_key_id = get_position_key_by_name(all_position, pos_key)
                        
                        # check key_data all match.
                        is_component_is_resource = False
                        use_orginal_glyph_instead_of_component = False

                        supported_position_key = "%d_%d" % (pos_key_id,ord(pos_data))

                        # get related glyph
                        related_glyph_list = get_related_glyph_list(supported_position_key,supported_position_set,supported_position_dict,skip_list)
                        related_glyph_length = len(related_glyph_list)

                        if SHOW_DEBUG_MESSAGE:
                            print("pos_data:", pos_data)
                            print("related_glyph_length:", related_glyph_length)

                        if related_glyph_length == 0:
                            # fail, try to use orginal component.
                            if ord(pos_data) in ff_unicode_set:
                                is_component_is_resource = True
                                use_orginal_glyph_instead_of_component = True
                            else:
                                if SHOW_DEBUG_MESSAGE:
                                    print("無本尊資料在字體檔，到別人家去借看看.")
                                # maybe try others key.
                                try_keys = ['左','右','上','下','右上','左下']
                                for try_key in try_keys:
                                    pos_key_id = get_position_key_by_name(all_position, try_key)
                                    supported_position_key = "%d_%d" % (pos_key_id,ord(pos_data))
                                    #print("try others key:", supported_position_key)
                                    if supported_position_key in supported_position_set:
                                        is_component_is_resource = True
                                        if SHOW_DEBUG_MESSAGE:
                                            print("bingo 找到可以借的字:%s" % (try_key))
                                        # change default rule name to query exist component.
                                        rule_name = try_key

                                        related_glyph_list = get_related_glyph_list(supported_position_key,supported_position_set,supported_position_dict,skip_list)
                                        related_glyph_length = len(related_glyph_list)

                                        break

                        else:
                            is_component_is_resource = True

                        # special case, 遇到'叕'時，使用原始物件。
                        # 因為，會猜的比較準。
                        if pos_data == '叕':
                            if ord(pos_data) in ff_unicode_set:
                                rule_name = "全"
                                is_component_is_resource = True
                                use_orginal_glyph_instead_of_component = True

                        # 最佳化規則，比程式去拆其他的字的組件出來，使用 original 會較好。                    
                        if rule_name == '上':
                            prefer_original_list = '喜隹焦子隋隊龍微徵君春敄朔執敖敬敕敏厭強廣能彗為保亞薛邵惢壽厥萬賊庳逢叔衛辟就攸'
                            prefer_original_list += '者列動爾雋埶前'
                            if pos_data in prefer_original_list:
                                if ord(pos_data) in ff_unicode_set:
                                    rule_name = "全"
                                    is_component_is_resource = True
                                    use_orginal_glyph_instead_of_component = True

                        if rule_name == '下' or rule_name == '右下':
                            prefer_original_list = '喜朋君兔青惠思恩悤貴界卯卵元完安亢冬尞卑童重垂放於施今令合余召各良艮介'
                            prefer_original_list += '列全有辛屈律時參亏將朁堯龍微徵鮮穌辟電雷務向弟高空生參國囷因男' 
                            prefer_original_list += '芻倩情咠禺啓喬吞每毋毌能用富奄阿從劍復欮包昆交臽卓音條宛迕宣宜' 
                            prefer_original_list += '烝湯買路臺嘉喪袁叔閑閒間闌悶疑壹亞妾畢是光亥夆足肖孚采妥兔色免杲宗香扁音' 
                            prefer_original_list += '盒弇畐前欶溫要彖須敫單責寅黃詹賓壽殻殼坎襄麃龜離蹩斃類靈龠' 
                            prefer_original_list += '妻家族頻逢冒最曼曾滿采雋巴邑卒委焦鞠敖會積冗瓜且加圭行員來囷孤封歏' 
                            prefer_original_list += '倉寇冠尉吳圭果俞戔治到虎洪契皇怨員衰衷羔難離累翏強洪冢家齊齋齏齎齍韲鼠龜'
                            prefer_original_list += '甄賴賣夐魏異留兵莫會丙我'
                            if pos_data in prefer_original_list:
                                if ord(pos_data) in ff_unicode_set:
                                    rule_name = "全"
                                    is_component_is_resource = True
                                    use_orginal_glyph_instead_of_component = True

                        # 避開連體字。
                        if pos_data == '冉':
                            disable_related_keyword_list = '再'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '夫':
                            disable_related_keyword_list = '失'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '貝':
                            disable_related_keyword_list = '貞負'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1
                        # 避開連體字。
                        if pos_data == '巾':
                            disable_related_keyword_list = '币市吊帛'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '千':
                            disable_related_keyword_list = '舌'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '古':
                            disable_related_keyword_list = '克'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1
                        
                        # 避開連體字。
                        if pos_data == '貝':
                            disable_related_keyword_list = '頁'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1
                        
                        # 避開連體字。
                        if pos_data == '田':
                            disable_related_keyword_list = '男'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '非':
                            disable_related_keyword_list = '韭'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '土':
                            disable_related_keyword_list = '王里'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '水':
                            disable_related_keyword_list = '泉汞'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '田':
                            disable_related_keyword_list = '里男'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '勿':
                            disable_related_keyword_list = '易'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '皿':
                            disable_related_keyword_list = '血'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '食':
                            disable_related_keyword_list = '養'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '白':
                            disable_related_keyword_list = '百'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '用':
                            disable_related_keyword_list = '甬'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '匹':
                            disable_related_keyword_list = '甚'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '大':
                            disable_related_keyword_list = '天夭'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '小':
                            disable_related_keyword_list = '糸'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '夕':
                            disable_related_keyword_list = '歹'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1
                        
                        # 避開連體字。
                        if pos_data == '木':
                            disable_related_keyword_list = '禾'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1
                        # 避開連體字。
                        if pos_data == '力':
                            disable_related_keyword_list = '男'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1
                        # 避開連體字。
                        if pos_data == '目':
                            disable_related_keyword_list = '見貝'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                       # 避開連體字。
                        if pos_data == '日':
                            disable_related_keyword_list = '早'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '罒':
                            disable_related_keyword_list = '蜀'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '允':
                            disable_related_keyword_list = '充'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '口':
                            disable_related_keyword_list = '占吊'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '立':
                            disable_related_keyword_list = '辛'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1

                        # 避開連體字。
                        if pos_data == '王':
                            disable_related_keyword_list = '丟'
                            related_glyph_length = len(related_glyph_list)
                            idx_offset = 0
                            for related_idx in range(related_glyph_length):
                                related_char,strokes_total = related_glyph_list[related_idx - idx_offset]
                                if related_char in disable_related_keyword_list:
                                    del related_glyph_list[related_idx - idx_offset]
                                    idx_offset += 1


                        related_glyph_length = len(related_glyph_list)


                        # force use orginal
                        #print("use_orginal_glyph_instead_of_component:", use_orginal_glyph_instead_of_component)
                        if use_orginal_glyph_instead_of_component:
                            related_glyph_list = [(pos_data,1)]
                            related_glyph_length = 1

                        if not is_component_is_resource:
                            messsage = "fail at pos_key: %s, component: %s" % (pos_key,pos_data)
                            output_file.write(messsage + "\n")
                            if SHOW_DEBUG_MESSAGE:
                                print(messsage)
                            is_match_supported_set = False
                        else:
                            # able to auto compose:
                            
                            total_related_char = ""
                            if related_glyph_length > 0:
                                for related_char,strokes_total in related_glyph_list:
                                    total_related_char += related_char
                            messsage = "component: %s \n+--chars length: %d \n+--source chars: %s \n+--source chars info: %s" % (pos_data, related_glyph_length, total_related_char, str(related_glyph_list))
                            output_file.write(messsage + "\n")
                            if SHOW_DEBUG_MESSAGE:
                                print(messsage)

                            pair_result, combine_list = pair_related_char(working_ff, target_ff, shake_redical, ff_dict, dict_data, pos_key, rule_name, pos_data, related_glyph_list, use_orginal_glyph_instead_of_component, combine_list, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, tmp_ff, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_DEBUG_MESSAGE, output_file)
                            if SHOW_DEBUG_MESSAGE:
                                print("pair_related_char result:", pair_result)
                            # 所有的 related char 可能都會 try fail, 這時改用本尊試試。
                            if not pair_result:
                                if not use_orginal_glyph_instead_of_component:
                                    # try use original component.
                                    if ord(pos_data) in ff_unicode_set:
                                        if SHOW_DEBUG_MESSAGE:
                                            print('召換本尊出場: %s' % (pos_data))
                                        use_orginal_glyph_instead_of_component = True
                                        related_glyph_list = [(pos_data,1)]
                                        related_glyph_length = 1
                                        pair_result, combine_list = pair_related_char(working_ff, target_ff, shake_redical, ff_dict, dict_data, pos_key, rule_name, pos_data, related_glyph_list, use_orginal_glyph_instead_of_component, combine_list, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, tmp_ff, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_DEBUG_MESSAGE, output_file)
                                        if SHOW_DEBUG_MESSAGE:
                                            print("本尊 pair_result:", pair_result)


                    if compare_count < 2:
                        is_match_supported_set = False

            if is_match_supported_set:
                if len(combine_list) >=2:
                    merge_result, glyph_filepath = merge_component(target_ff, char, char_info_array, combine_list, file_index, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, SHOW_DEBUG_MESSAGE, output_file, add_extra_finetune_commands)
                    if merge_result:
                        file_index+=1
                pass
            else:
                if SHOW_DEBUG_MESSAGE:
                    print("not able to auto compose:", char)
                pass

    if len(total_lost_char_list) > 0:
        output_file.write(('=' * 40) + '\n')
        messsage = "Total lost char: %s" % (total_lost_char_list)
        output_file.write(messsage + "\n")

    output_file.close()

def main(args):
    # check input.
    pass_input_check = True
    error_message = ""

    # read configs.
    # main parameter.
    import_file = args.file
    working_ff = args.input
    target_ff = args.output

    # optional parameter
    tmp_ff = args.tmp
    skip_list_file = args.skip_list
    shake_redical = args.shake

    if pass_input_check:
        if not exists(working_ff):
            pass_input_check = False
            error_message = "source FontForge project folder not exist."

    if pass_input_check:
        if not exists(import_file):
            pass_input_check = False
            error_message = "compose list file not exist."

    if pass_input_check:
        if not exists(target_ff):
            mkdir(target_ff)

        if not exists(tmp_ff):
            mkdir(tmp_ff)

        target_font_props = join(target_ff,"font.props")
        if not exists(target_font_props):
            source_font_props = join(working_ff,"font.props")
            shutil.copy(source_font_props,target_font_props)

    dictionary_filepath = args.dictionary_file 
    if pass_input_check:
        if not exists(dictionary_filepath):
            pass_input_check = False
            error_message = "dictionary file not exist, please download it from github."
        else:
            print("file exist:", dictionary_filepath)
            pass

    # Optional input file.
    thin_component_filepath = args.thin_component
    heavy_component_filepath = args.heavy_component
    skip_average_redical_filepath = args.skip_average_redical
    
    log_filepath = args.log_file

    if args.clean == "True":
        clean_target(target_ff)
        clean_target(tmp_ff)

    # from 1 to 3.
    UNICODE_FIELD = 1       # default
    UNICODE_FIELD = 2       # for Noto Sans

    add_extra_finetune_commands = args.add_extra_finetune_commands
    if pass_input_check:
        # get working ff infos.
        ff_unicode_set, ff_dict, GLYPH_WIDTH, GLYPH_UNDERLINE = get_font_info(working_ff, UNICODE_FIELD)
        # get supported_position_set
        dict_data, all_position, supported_position_set, supported_position_dict = travel_preprocess(ff_unicode_set, dictionary_filepath)
        # load config files.
        target_chars_list, skip_list, THIN_COMPONENT,HEAVY_COMPONENT,skip_average_mode_redical_list = load_config_files(import_file, skip_list_file, thin_component_filepath, heavy_component_filepath, skip_average_redical_filepath)

        SHOW_DEBUG_MESSAGE = False
        if args.debug == "True":
            SHOW_DEBUG_MESSAGE = True   # debug.

        print("compare with lost target chars...")
        print("import chars list file:", import_file)
        print("import chars length:", len(target_chars_list))
        print("skip chars length:", len(skip_list))
    
        travel_glyph(target_ff, working_ff, tmp_ff, dict_data, target_chars_list, skip_list, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, ff_unicode_set, ff_dict, all_position, supported_position_set, supported_position_dict, shake_redical, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, SHOW_DEBUG_MESSAGE, log_filepath, add_extra_finetune_commands)

        if args.preview == "True":
            preview(target_ff)
    else:
        print(error_message)


def cli():
    parser = argparse.ArgumentParser(
            description="auto compose glyph")

    parser.add_argument("--input",
        help="input font sfdir folder",
        required=True,
        type=str)

    parser.add_argument("--tmp",
        help="tmp font sfdir folder",
        default='tmp.sfdir',
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default='new.sfdir',
        type=str)

    parser.add_argument("--file",
        help="lost chars file to auto compose",
        default='ff_import.txt',
        required=True,
        type=str)

    parser.add_argument("--skip_list",
        help="verified glyph not able to reuse in this font",
        default='ff_skip_list.txt',
        type=str)

    parser.add_argument("--thin_component",
        help="thin component",
        default='ff_thin_component.txt',
        type=str)

    parser.add_argument("--heavy_component",
        help="heavy component",
        default='ff_heavy_component.txt',
        type=str)

    parser.add_argument("--skip_average_redical",
        help="redical don't use average mode component",
        default='ff_skip_average_mode_redical.txt',
        type=str)

    #PS: this is TODO feature, not implement now.
    parser.add_argument("--reuse_component",
        help="verified reuse component",
        default='reuse.sfdir',
        type=str)

    parser.add_argument("--clean",
        help="clean glyphs before re-transform",
        default='True',
        type=str)

    parser.add_argument("--preview",
        help="user ff to preview",
        default='True',
        type=str)

    parser.add_argument("--debug",
        help="show debug info",
        action='store_true')

    parser.add_argument("--log_file",
        help="travel log filename",
        default='compose.log',
        type=str)

    parser.add_argument("--dictionary_file",
        help="dictionary json file path",
        default='Dictionary_lite.json',
        type=str)

    parser.add_argument("--shake",
        help="shake redical for handwriting font",
        default='True',
        type=str)

    parser.add_argument("--add_extra_finetune_commands",
        help="add extra commands for some second glyph",
        action='store_true')


    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()
