#!/usr/bin/env python3
#encoding=utf-8

import os
from os.path import join, exists
import argparse

def apply_transform_command(x,y,cmd_array):
    # apply command.
    if cmd_array[0]=="MOVE":
        offset = int(float(cmd_array[3]))
        if "X" in cmd_array[2]:
            x += offset
        if "Y" in cmd_array[2]:
            y += offset

    if cmd_array[0]=="SCALE":
        percent = float(cmd_array[3])
        if "X" in cmd_array[2]:
            x = int(x * percent)
        if "Y" in cmd_array[2]:
            y = int(y * percent)
    return x,y

def transform_stroke(stroke_dict, cmd_array):
    default_int = -9999

    # before move center.
    center_x , center_y = 0,0
    if cmd_array[0] ==  "SCALE":
        glyph_margin = compute_stroke_margin(stroke_dict)
        center_x , center_y = int((glyph_margin["left"] + glyph_margin["right"])/2), int((glyph_margin["top"] + glyph_margin["bottom"])/2)
        #print("center_x , center_y:", center_x , center_y)

    for key in stroke_dict.keys():
        #print("key:", key)
        spline_dict = stroke_dict[key]

        #print("spline_dict:", spline_dict)
        for dot_dict in spline_dict['dots']:
            new_line = dot_dict['code']
            x_line_array = new_line.split(' ')
            t = dot_dict['t']
            x,y=default_int,default_int
            x1,y1=default_int,default_int
            x2,y2=default_int,default_int
            if t=='m':
                x=int(float(x_line_array[0]))
                y=int(float(x_line_array[1]))

                x,y = apply_transform_command(x,y,cmd_array)

                x_line_array[0]=str(x)
                x_line_array[1]=str(y)

            if t=='l':
                x=int(float(x_line_array[1]))
                y=int(float(x_line_array[2]))

                x,y = apply_transform_command(x,y,cmd_array)

                x_line_array[1]=str(x)
                x_line_array[2]=str(y)

            if t=='c':
                if len(x_line_array) >=7:
                    x=int(float(x_line_array[5]))
                    y=int(float(x_line_array[6]))
                    x1=int(float(x_line_array[1]))
                    y1=int(float(x_line_array[2]))
                    x2=int(float(x_line_array[3]))
                    y2=int(float(x_line_array[4]))

                    x,y = apply_transform_command(x,y,cmd_array)
                    x1,y1 = apply_transform_command(x1,y1,cmd_array)
                    x2,y2 = apply_transform_command(x2,y2,cmd_array)

                    x_line_array[1]=str(x1)
                    x_line_array[2]=str(y1)
                    x_line_array[3]=str(x2)
                    x_line_array[4]=str(y2)
                    x_line_array[5]=str(x)
                    x_line_array[6]=str(y)

                    dot_dict['x1']=x1
                    dot_dict['y1']=y1
                    dot_dict['x2']=x2
                    dot_dict['y2']=y2

            dot_dict['x']=x
            dot_dict['y']=y

            new_code = ' '.join(x_line_array)
            dot_dict['code'] = new_code

    if cmd_array[0] ==  "SCALE":
        glyph_margin = compute_stroke_margin(stroke_dict)
        after_center_x , after_center_y = int((glyph_margin["left"] + glyph_margin["right"])/2), int((glyph_margin["top"] + glyph_margin["bottom"])/2)
        #print("after_center_x , after_center_y:", after_center_x , after_center_y)

        new_transform_cmd = ['MOVE','','X',center_x - after_center_x]
        transform_stroke(stroke_dict,new_transform_cmd)
        new_transform_cmd = ['MOVE','','Y',center_y - after_center_y]
        transform_stroke(stroke_dict,new_transform_cmd)

def load_to_memory(filename_input):
    # return field.
    stroke_dict = {}
    encoding_string = None
    
    dot_dict = {}
    dots_array = []
    default_int = -9999

    #print("load to memory, filename_input:", filename_input)
    myfile = open(filename_input, 'r')

    code_encoding_string = 'Encoding: '
    code_encoding_string_length = len(code_encoding_string)

    code_begin_string = 'SplineSet'
    code_begin_string_length = len(code_begin_string)

    code_end_string = 'EndSplineSet'
    code_end_string_length = len(code_end_string)

    is_code_flag=False

    stroke_index = 0

    for x_line in myfile:
        if code_encoding_string == x_line[:code_encoding_string_length]:
            encoding_string = x_line[code_encoding_string_length:]

        if not is_code_flag:
            # check begin.

            if code_begin_string == x_line[:code_begin_string_length]:
                is_code_flag = True
        else:
            # is code start.
            #print("x_line:", x_line)

            if x_line[:1] != ' ':
                if stroke_index >= 1:
                    stroke_dict[stroke_index]={}
                    stroke_dict[stroke_index]['dots'] = dots_array
                    #if stroke_index == 1:
                        #print("key:", stroke_index, "data:", stroke_dict)
                    
                    # reset new
                    dots_array = []

                stroke_index += 1

            # check end
            if code_end_string == x_line[:code_end_string_length]:
                #is_code_flag = False
                break

            dot_dict = {}

            # type
            t=''
            if ' m ' in x_line:
                t='m'
            if ' l ' in x_line:
                t='l'
            if ' c ' in x_line:
                t='c'
            dot_dict['t']=t

            x=default_int
            y=default_int
            x1=default_int
            y1=default_int
            x2=default_int
            y2=default_int

            # need format code to "ROUND int"
            new_code = ""
            if ' ' in x_line:
                x_line_array = x_line.split(' ')
                if t=='m':
                    x=int(float(x_line_array[0]))
                    y=int(float(x_line_array[1]))

                    x_line_array[0]=str(x)
                    x_line_array[1]=str(y)

                if t=='l':
                    x=int(float(x_line_array[1]))
                    y=int(float(x_line_array[2]))

                    x_line_array[1]=str(x)
                    x_line_array[2]=str(y)

                if t=='c':
                    if len(x_line_array) >=7:
                        x=int(float(x_line_array[5]))
                        y=int(float(x_line_array[6]))
                        x1=int(float(x_line_array[1]))
                        y1=int(float(x_line_array[2]))
                        x2=int(float(x_line_array[3]))
                        y2=int(float(x_line_array[4]))

                        x_line_array[1]=str(x1)
                        x_line_array[2]=str(y1)
                        x_line_array[3]=str(x2)
                        x_line_array[4]=str(y2)
                        x_line_array[5]=str(x)
                        x_line_array[6]=str(y)

                #print("add to code:", x_line)
                #dot_dict['code'] = x_line
                new_code = ' '.join(x_line_array)
            dot_dict['code'] = new_code


            dot_dict['x']=x
            dot_dict['y']=y

            dot_dict['x1']=x1
            dot_dict['y1']=y1
            dot_dict['x2']=x2
            dot_dict['y2']=y2

            dots_array.append(dot_dict)

    myfile.close()
    return stroke_dict, encoding_string

def write_to_file(filename_input, stroke_dict):
    filename_input_new = filename_input + ".tmp"

    myfile = open(filename_input, 'r')
    myfile_new = open(filename_input_new, 'w')
    code_begin_string = 'SplineSet'
    code_begin_string_length = len(code_begin_string)
    code_end_string = 'EndSplineSet'
    code_end_string_length = len(code_end_string)

    is_code_flag=False

    stroke_index = 0
    #print("write_to_file:", filename_input)
    for x_line in myfile:
        #print("x_line:", x_line)
        if not is_code_flag:
            # check begin.

            if code_begin_string == x_line[:code_begin_string_length]:
                is_code_flag = True
            myfile_new.write(x_line)

        else:
            # check end
            if code_end_string == x_line[:code_end_string_length]:
                #print("code_end_string:", x_line)

                is_code_flag = False

                #flush memory to disk
                for key in stroke_dict.keys():
                    #print("key:", key)
                    spline_dict = stroke_dict[key]
                    #print("spline_dict:", spline_dict)
                    for dot_dict in spline_dict['dots']:
                        new_line = dot_dict['code']
                        myfile_new.write(new_line)

                myfile_new.write(x_line)
                #break

    myfile.close()
    myfile_new.close()

    os.remove(filename_input)
    os.rename(filename_input_new, filename_input)

    return stroke_dict

def get_stroke_dict(filename_input,UNICODE_FIELD, transform_commands=[]):
    stroke_dict = {}
    encoding_string = None
    stroke_dict, encoding_string = load_to_memory(filename_input)
    
    for cmd in transform_commands:
        if ":" in cmd:
            cmd_array = cmd.split(':')
            if cmd_array[0] in ['SCALE','MOVE']:
                transform_stroke(stroke_dict, cmd_array)

    unicode_int = -1
    if not encoding_string is None:
        if ' ' in encoding_string:
            encoding_string_array = encoding_string.split(' ')
            unicode_string = encoding_string_array[UNICODE_FIELD-1]
            if len(unicode_string) > 0:
                unicode_int = int(unicode_string)

    return stroke_dict, unicode_int

def detect_margin(spline_dict):
    default_int = -9999

    margin_top=default_int
    margin_bottom=default_int
    margin_left=default_int
    margin_right=default_int

    average_x = -9999
    average_y = -9999
    total_x = 0
    total_y = 0

    dot_idx = 0
    for dot_dict in spline_dict['dots']:
        dot_idx += 1
        x=dot_dict['x']

        if x != default_int:
            total_x += x
            
            if margin_right==default_int:
                # initail assign
                margin_right=x
            else:
                # compare top
                if x > margin_right:
                    margin_right = x

            if margin_left==default_int:
                # initail assign
                margin_left=x
            else:
                # compare bottom
                if x < margin_left:
                    margin_left = x

        y=dot_dict['y']
        if y !=default_int:
            total_y += y

            if margin_top==default_int:
                # initail assign
                margin_top=y
            else:
                # compare top
                if y > margin_top:
                    margin_top = y

            if margin_bottom==default_int:
                # initail assign
                margin_bottom=y
            else:
                # compare bottom
                if y < margin_bottom:
                    margin_bottom = y

    if dot_idx > 0:
        average_x = int(total_x / dot_idx)
        average_y = int(total_y / dot_idx)

    spline_dict["top"]  = margin_top
    spline_dict["bottom"] = margin_bottom
    spline_dict["left"] = margin_left
    spline_dict["right"] = margin_right
    spline_dict["average_x"] = average_x
    spline_dict["average_y"] = average_y

def compute_stroke_margin(stroke_dict):
    #print("trace_stroke")
    #print(stroke_dict)

    glyph_margin={}

    glyph_margin["top"]  = None
    glyph_margin["bottom"] = None
    glyph_margin["left"] = None
    glyph_margin["right"] = None

    if 1 in stroke_dict:
       for key in stroke_dict.keys():
            spline_dict = stroke_dict[key]
            detect_margin(spline_dict)

            if glyph_margin["top"] is None:
                glyph_margin["top"]  = stroke_dict[key]["top"]
                glyph_margin["bottom"] = stroke_dict[key]["bottom"]
                glyph_margin["left"] = stroke_dict[key]["left"]
                glyph_margin["right"] = stroke_dict[key]["right"]

            if glyph_margin["top"] < spline_dict["top"]:
                glyph_margin["top"]  = spline_dict["top"]
            if glyph_margin["bottom"] > spline_dict["bottom"]:
                glyph_margin["bottom"] = spline_dict["bottom"]
            if glyph_margin["left"] > spline_dict["left"]:
                glyph_margin["left"] = spline_dict["left"]
            if glyph_margin["right"] < spline_dict["right"]:
                glyph_margin["right"] = spline_dict["right"]

    return glyph_margin

def check_clockwise(spline_dict):
    clockwise = True
    area_total=0
    poly_lengh = len(spline_dict['dots'])
    #print('check poly: (%d,%d)' % (poly[0][0],poly[0][1]))
    for idx in range(poly_lengh):
        #item_sum = ((poly[(idx+1)%poly_lengh][0]-poly[(idx+0)%poly_lengh][0]) * (poly[(idx+1)%poly_lengh][1]-poly[(idx+0)%poly_lengh][1]))
        item_sum = ((spline_dict['dots'][(idx+0)%poly_lengh]['x']*spline_dict['dots'][(idx+1)%poly_lengh]['y']) - (spline_dict['dots'][(idx+1)%poly_lengh]['x']*spline_dict['dots'][(idx+0)%poly_lengh]['y']))
        #print(idx, poly[idx][0], poly[idx][1], item_sum)
        area_total += item_sum
    #print("area_total:",area_total)
    if area_total >= 0:
        clockwise = not clockwise
    return clockwise

def check_left_right_overlap(stroke_dict_1, stroke_dict_2):
    is_overlap = False
    overlap_length = 0

    glyph_margin_1 = compute_stroke_margin(stroke_dict_1)
    #print("1 left,right", glyph_margin_1["left"] , glyph_margin_1["right"])
    glyph_margin_2 = compute_stroke_margin(stroke_dict_2)
    #print("2 left,right", glyph_margin_2["left"] , glyph_margin_2["right"])

    if glyph_margin_2["left"] < glyph_margin_1["right"]:
        is_overlap = True

    overlap_length = glyph_margin_1["right"] - glyph_margin_2["left"]

    return is_overlap, overlap_length, glyph_margin_1, glyph_margin_2

def check_top_bottom_overlap(stroke_dict_1, stroke_dict_2):
    is_overlap = False
    overlap_length = 0

    glyph_margin_1 = compute_stroke_margin(stroke_dict_1)
    #print("1 left,right", glyph_margin_1["left"] , glyph_margin_1["right"])
    glyph_margin_2 = compute_stroke_margin(stroke_dict_2)
    #print("2 left,right", glyph_margin_2["left"] , glyph_margin_2["right"])

    if glyph_margin_2["top"] > glyph_margin_1["bottom"]:
        is_overlap = True

    overlap_length = glyph_margin_2["top"] - glyph_margin_1["bottom"]

    return is_overlap, overlap_length, glyph_margin_1, glyph_margin_2

def adjust_left_right(stroke_dict_1, stroke_dict_2, GLYPH_WIDTH):
    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
    #print("#1 is_overlap, overlap_length:", is_overlap, overlap_length)

    # split two spline
    # fit long side.
    left_margin = int(GLYPH_WIDTH * 0.1)
    if is_overlap:
        for idx in range(20):
            if glyph_margin_1["left"] >= left_margin:
                new_transform_cmd = ['MOVE','','X', -1 * (left_margin * 0.1)]
                transform_stroke(stroke_dict_1,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break
    if is_overlap:
        for idx in range(20):
            if (GLYPH_WIDTH - glyph_margin_2["right"]) >= left_margin:
                new_transform_cmd = ['MOVE','','X', (left_margin * 0.1)]
                transform_stroke(stroke_dict_2,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break

    # fit short side.
    left_margin_short = int(GLYPH_WIDTH * 0.05)
    if is_overlap:
        for idx in range(20):
            if glyph_margin_1["left"] >= left_margin_short:
                new_transform_cmd = ['MOVE','','X', -1 * (left_margin * 0.1)]
                transform_stroke(stroke_dict_1,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break
    if is_overlap:
        for idx in range(20):
            if (GLYPH_WIDTH - glyph_margin_2["right"]) >= left_margin_short:
                new_transform_cmd = ['MOVE','','X', (left_margin * 0.1)]
                transform_stroke(stroke_dict_2,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break

    # still
    allow_overlap_gap = int(GLYPH_WIDTH * 0.004)
    left_side_long_threshold = int(GLYPH_WIDTH * 0.43)
    right_side_long_threshold = int(GLYPH_WIDTH * 0.55)
    #print("overlap_length:", overlap_length)
    for idx in range(10):
        if is_overlap:
            if overlap_length >= allow_overlap_gap:
                if glyph_margin_1["right"] - glyph_margin_1["left"] > left_side_long_threshold:
                    # to avoid "皋" become very small
                    if idx <= 1:
                        new_transform_cmd = ['SCALE','','XY', 0.95]
                    else:
                        new_transform_cmd = ['SCALE','','X', 0.95]
                    transform_stroke(stroke_dict_1,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
        # still
        if is_overlap:
            if overlap_length >= allow_overlap_gap:
                if glyph_margin_2["right"] - glyph_margin_2["left"] > right_side_long_threshold:
                    if idx <= 1:
                        new_transform_cmd = ['SCALE','','XY', 0.95]
                    else:
                        new_transform_cmd = ['SCALE','','X', 0.95]
                    transform_stroke(stroke_dict_2,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)

        # split.
        if is_overlap:
            for idx in range(2):
                #print("glyph_margin_1[left]:", glyph_margin_1["left"])
                if glyph_margin_1["left"] >= left_margin_short:
                    new_transform_cmd = ['MOVE','','X', -1 * (left_margin * 0.1)]
                    transform_stroke(stroke_dict_1,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
                    if not is_overlap:
                        break
                else:
                    break

        if is_overlap:
            for idx in range(2):
                #print("glyph_margin_1[left]:", glyph_margin_1["left"])
                if (GLYPH_WIDTH - glyph_margin_2["right"]) >= left_margin_short:
                    new_transform_cmd = ['MOVE','','X', (left_margin * 0.1)]
                    transform_stroke(stroke_dict_2,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)
                    if not is_overlap:
                        break
                else:
                    break

    # too far.
    too_close_distance = -1 * int(GLYPH_WIDTH * 0.08)
    #print("#2 is_overlap, overlap_length:", is_overlap, overlap_length)

    for idx in range(4):
        if overlap_length < too_close_distance:
            new_transform_cmd = ['MOVE','','X', (left_margin * 0.1)]
            transform_stroke(stroke_dict_1,new_transform_cmd)
            is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)

        if overlap_length < too_close_distance:
            new_transform_cmd = ['MOVE','','X', -1 * (left_margin * 0.1)]
            transform_stroke(stroke_dict_2,new_transform_cmd)
            is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_left_right_overlap(stroke_dict_1, stroke_dict_2)

def adjust_top_bottom(stroke_dict_1, stroke_dict_2, GLYPH_WIDTH, GLYPH_UNDERLINE):
    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
    #print("#1 is_overlap, overlap_length:", is_overlap, overlap_length)

    # split two spline
    # fit long side.
    left_margin = int(GLYPH_WIDTH * 0.15)
    top_margin = (GLYPH_WIDTH - left_margin) + GLYPH_UNDERLINE
    bottom_margin = left_margin + GLYPH_UNDERLINE

    if is_overlap:
        for idx in range(20):
            if glyph_margin_1["top"] <= top_margin:
                new_transform_cmd = ['MOVE','','Y', +1 * (left_margin * 0.1)]
                transform_stroke(stroke_dict_1,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break
    if is_overlap:
        for idx in range(20):
            if (glyph_margin_2["bottom"]) >= bottom_margin:
                new_transform_cmd = ['MOVE','','Y', -1 * (left_margin * 0.1)]
                transform_stroke(stroke_dict_2,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break

    # fit short side.
    left_margin_short = int(GLYPH_WIDTH * 0.10)
    top_margin = (GLYPH_WIDTH - left_margin_short) + GLYPH_UNDERLINE
    bottom_margin = left_margin_short + GLYPH_UNDERLINE

    if is_overlap:
        for idx in range(20):
            if glyph_margin_1["top"] <= top_margin:
                new_transform_cmd = ['MOVE','','Y', +1 * (left_margin * 0.1)]
                transform_stroke(stroke_dict_1,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break
    if is_overlap:
        for idx in range(20):
            if (glyph_margin_2["bottom"]) >= bottom_margin:
                new_transform_cmd = ['MOVE','','Y', -1 * (left_margin * 0.1)]
                transform_stroke(stroke_dict_2,new_transform_cmd)
                is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
                if not is_overlap:
                    break
            else:
                break

    # still
    allow_overlap_gap = int(GLYPH_WIDTH * 0.002)

    # depend on the stroke count. from 2.5 to 3.5
    left_side_long_threshold = int(GLYPH_WIDTH * 0.34)
    right_side_long_threshold = int(GLYPH_WIDTH * 0.55)

    top_margin = (GLYPH_WIDTH - left_margin_short) + GLYPH_UNDERLINE
    bottom_margin = left_margin_short + GLYPH_UNDERLINE

    #print("#2 overlap_length:", overlap_length)
    for idx in range(10):
        if is_overlap:
            if overlap_length >= allow_overlap_gap:
                if glyph_margin_1["top"] - glyph_margin_1["bottom"] > left_side_long_threshold:
                    # to avoid "皋" become very small
                    if idx <= 2:
                        new_transform_cmd = ['SCALE','','XY', 0.95]
                    else:
                        new_transform_cmd = ['SCALE','','Y', 0.95]
                    transform_stroke(stroke_dict_1,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
        # still
        if is_overlap:
            if overlap_length >= allow_overlap_gap:
                if glyph_margin_2["top"] - glyph_margin_2["bottom"] > right_side_long_threshold:
                    if idx <= 2:
                        new_transform_cmd = ['SCALE','','XY', 0.95]
                    else:
                        new_transform_cmd = ['SCALE','','Y', 0.95]
                    transform_stroke(stroke_dict_2,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)

        # split.
        if is_overlap:
            for idx in range(2):
                #print("glyph_margin_1[left]:", glyph_margin_1["top"])
                if glyph_margin_1["top"] <= top_margin:
                    new_transform_cmd = ['MOVE','','Y', +1 * (left_margin * 0.1)]
                    transform_stroke(stroke_dict_1,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
                    if not is_overlap:
                        break
                else:
                    break

        if is_overlap:
            for idx in range(2):
                #print("glyph_margin_1[left]:", glyph_margin_1["top"])
                if (glyph_margin_2["bottom"]) >= bottom_margin:
                    new_transform_cmd = ['MOVE','','Y', -1 * (left_margin * 0.1)]
                    transform_stroke(stroke_dict_2,new_transform_cmd)
                    is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)
                    if not is_overlap:
                        break
                else:
                    break

    # too far.
    too_close_distance = -1 * int(GLYPH_WIDTH * 0.08)
    #print("#3 is_overlap, overlap_length:", is_overlap, overlap_length)

    for idx in range(4):
        if overlap_length < too_close_distance:
            new_transform_cmd = ['MOVE','','Y', -1 * (left_margin * 0.1)]
            transform_stroke(stroke_dict_1,new_transform_cmd)
            is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)

        if overlap_length < too_close_distance:
            new_transform_cmd = ['MOVE','','Y', +1 * (left_margin * 0.1)]
            transform_stroke(stroke_dict_2,new_transform_cmd)
            is_overlap, overlap_length, glyph_margin_1, glyph_margin_2 = check_top_bottom_overlap(stroke_dict_1, stroke_dict_2)

def merge_stroke(stroke_dict_1, stroke_dict_2, component_rule, GLYPH_WIDTH, GLYPH_UNDERLINE, add_extra_finetune_commands):
    intersection_dict = {}

    SHOW_DEBUG_MESSAGE = False
    #SHOW_DEBUG_MESSAGE = True   # debug.


    if add_extra_finetune_commands:
        # finetune
        if component_rule=='左右':
            adjust_left_right(stroke_dict_1, stroke_dict_2, GLYPH_WIDTH)

        if component_rule=='上下':
            adjust_top_bottom(stroke_dict_1, stroke_dict_2, GLYPH_WIDTH, GLYPH_UNDERLINE)

    if 1 in stroke_dict_1:
       for key_1 in stroke_dict_1.keys():
            is_add_spline = True

            spline_dict_1 = stroke_dict_1[key_1]

            new_key_index = len(intersection_dict)+1
            intersection_dict[new_key_index]=spline_dict_1.copy()
            is_found_component = True

    if 1 in stroke_dict_2:
       for key_2 in stroke_dict_2.keys():
            spline_dict_2 = stroke_dict_2[key_2]

            new_key_index = len(intersection_dict)+1
            intersection_dict[new_key_index]=spline_dict_2.copy()
            is_found_component = True

    return is_found_component, intersection_dict

def get_intersection(stroke_dict_1, stroke_dict_2):
    is_found_component = False

    # 複雜形狀，允許誤差高。
    AVERAGE_ACCURACY_POLY = 100
    # 簡易形狀，允許誤差低。
    AVERAGE_ACCURACY_SIMPLE = 50
    # 簡易形狀的點數
    SIMPLE_THRESHOLD = 6

    MARGIN_ACCURACY = 120
    LENGTH_ACCURACY = 12

    intersection_dict = {}

    SHOW_DEBUG_MESSAGE = False
    #SHOW_DEBUG_MESSAGE = True   # debug.

    if 1 in stroke_dict_1:
       for key_1 in stroke_dict_1.keys():
            is_add_spline = False

            spline_dict_1 = stroke_dict_1[key_1]
            spline_dict_1_code_length = len(spline_dict_1['dots'])
            clockwise_1 = check_clockwise(spline_dict_1)
            if SHOW_DEBUG_MESSAGE:
                print("spline_dict_1_code_length:", spline_dict_1_code_length)
                print("margin:",spline_dict_1["top"],spline_dict_1["left"],spline_dict_1["bottom"],spline_dict_1["right"])
                print("average:",spline_dict_1["average_x"],spline_dict_1["average_y"])

            if 1 in stroke_dict_2:
               for key_2 in stroke_dict_2.keys():
                    spline_dict_2 = stroke_dict_2[key_2]
                    spline_dict_2_code_length = len(spline_dict_2['dots'])
                    clockwise_2 = check_clockwise(spline_dict_2)
                    if SHOW_DEBUG_MESSAGE:
                        print("spline_dict_2_code_length:", spline_dict_2_code_length)
                        print("margin:",spline_dict_2["top"],spline_dict_2["left"],spline_dict_1["bottom"],spline_dict_2["right"])
                        print("average:",spline_dict_2["average_x"],spline_dict_2["average_y"])

                    fail_code = 100
                    if clockwise_1 == clockwise_2:
                        fail_code = 110
                        if abs(spline_dict_1_code_length - spline_dict_2_code_length) <= LENGTH_ACCURACY:
                            fail_code = 120
                            if abs(spline_dict_2["top"]-spline_dict_1["top"]) <= MARGIN_ACCURACY:
                                fail_code = 130
                                if abs(spline_dict_2["left"]-spline_dict_1["left"]) <= MARGIN_ACCURACY:
                                    fail_code = 140
                                    if abs(spline_dict_2["bottom"]-spline_dict_1["bottom"]) <= MARGIN_ACCURACY:
                                        fail_code = 150
                                        if abs(spline_dict_2["right"]-spline_dict_1["right"]) <= MARGIN_ACCURACY:
                                            fail_code = 160
                                            if spline_dict_2_code_length <= SIMPLE_THRESHOLD:
                                                # simple rule
                                                fail_code = 170
                                                if abs(spline_dict_2["average_x"]-spline_dict_1["average_x"]) <= AVERAGE_ACCURACY_SIMPLE:
                                                    fail_code = 171
                                                    if abs(spline_dict_2["average_y"]-spline_dict_1["average_y"]) <= AVERAGE_ACCURACY_SIMPLE:
                                                        is_add_spline = True
                                            else:
                                                # complex rule
                                                fail_code = 180
                                                if abs(spline_dict_2["average_x"]-spline_dict_1["average_x"]) <= AVERAGE_ACCURACY_POLY:
                                                    fail_code = 181
                                                    if abs(spline_dict_2["average_y"]-spline_dict_1["average_y"]) <= AVERAGE_ACCURACY_POLY:
                                                        is_add_spline = True

                    if not is_add_spline:
                        if SHOW_DEBUG_MESSAGE:
                            print("fail code:", fail_code)
                        pass
                    else:
                        if SHOW_DEBUG_MESSAGE:
                            print("bingo!")
                        new_key_index = len(intersection_dict)+1
                        intersection_dict[new_key_index]=spline_dict_1.copy()
                        is_found_component = True

                        break

    return is_found_component, intersection_dict

def get_component(parse_char, dict_data, stroke_dict_1, glyph_margin, component, rule_name, GLYPH_WIDTH, GLYPH_UNDERLINE, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_DEBUG_MESSAGE):
    is_found_component = False

    MARGIN_ACCURACY = 100

    intersection_dict = {}

    #SHOW_DEBUG_MESSAGE = False
    #SHOW_DEBUG_MESSAGE = True   # debug.

    if SHOW_DEBUG_MESSAGE:
        print("process, rule_name:", rule_name, "component:", component)

    is_match_component_rule = False
    # 有筆畫相連
    is_critical_fail = False

    if 1 in stroke_dict_1:

        # get component stroke count.
        strokes_total = -1
        if component in dict_data:
            char_dict=dict_data[component]
            if 'strokes_total' in char_dict:
                strokes_total = char_dict['strokes_total']

        # get process char radical.
        char_radical = None
        if parse_char in dict_data:
            char_dict=dict_data[parse_char]
            if 'radical' in char_dict:
                char_radical = char_dict['radical']

        if SHOW_DEBUG_MESSAGE:
            print("component strokes_total:", strokes_total)
            print("char_radical:", char_radical)

        MAP_X_CENTER = int(GLYPH_WIDTH * 0.5)
        MAP_Y_CENTER = int((GLYPH_WIDTH * 0.5)+GLYPH_UNDERLINE)

        # is this component use thin rule.
        # 筆劃較少
        use_thin_stroke_rule = False
        if component in THIN_COMPONENT:
            use_thin_stroke_rule = True
        if strokes_total <= 5 and strokes_total >= 1:
            use_thin_stroke_rule = True
        
        # 筆劃較多
        use_complex_stroke_rule = False
        if not use_thin_stroke_rule:
            # 因為 thin list 裡的項目會超過 strokes_total 會被 overwrite.
            if strokes_total >= 10:
                use_complex_stroke_rule = True

        # force use havey if in the list.
        if component in HEAVY_COMPONENT:
            use_complex_stroke_rule = True
            use_thin_stroke_rule = False

        if SHOW_DEBUG_MESSAGE:
            print("use_complex_stroke_rule:", use_complex_stroke_rule)
            print("use_thin_stroke_rule:", use_thin_stroke_rule)


        for key_1 in stroke_dict_1.keys():
            is_add_spline = False

            spline_dict_1 = stroke_dict_1[key_1]
            spline_dict_1_code_length = len(spline_dict_1['dots'])
            #clockwise = check_clockwise(spline_dict_1)
            if SHOW_DEBUG_MESSAGE:
                print("spline_dict_1_code_length:", spline_dict_1_code_length)
                print("spline code:", spline_dict_1['dots'][0]['code'].strip())
                print("margin top,left,bottom,right:",spline_dict_1["top"],spline_dict_1["left"],spline_dict_1["bottom"],spline_dict_1["right"])
                print("average:",spline_dict_1["average_x"],spline_dict_1["average_y"])
                #print("clockwise:", clockwise)

            # ==============================
            # 第1組合, ex: 姚
            # ==============================
            # PS: 有些手寫字體，左右二邊重心都偏中間。造成拆解很容易誤判！
            spline_fail_code = -1
            if rule_name == '左':
                spline_fail_code = 100

                MAP_THRESHOLD = int(GLYPH_WIDTH * 0.5)
                
                if use_thin_stroke_rule:
                    MAP_THRESHOLD = int(GLYPH_WIDTH * 0.385)
                if use_complex_stroke_rule:
                    MAP_THRESHOLD = int(GLYPH_WIDTH * 0.66)
                
                if SHOW_DEBUG_MESSAGE:
                    print('MAP_THRESHOLD:', MAP_THRESHOLD)
                if spline_dict_1["right"] <= (MAP_THRESHOLD + 0):
                    spline_fail_code = 110
                    is_add_spline = True
                
                # or
                # left must more the this limit.
                MAP_LEFT_MIN = int(GLYPH_WIDTH * 0.3)
                if strokes_total >= 10:
                    # 筆劃較多
                    MAP_LEFT_MIN = int(GLYPH_WIDTH * 0.55)

                # 例外：允許超過 threshold 的，但重心在左邊。
                if not is_add_spline:
                    if spline_dict_1["average_x"] <= (MAP_X_CENTER - 0):
                        spline_fail_code = 120
                        is_add_spline = True

                        FAIL_THRESHOLD = int(GLYPH_WIDTH * 0.667)
                        # 如果找到了，但..., 連在一起了. 
                        if spline_dict_1["right"] >= (FAIL_THRESHOLD + 0):
                            spline_fail_code = 130
                            is_add_spline = False

                            # 左邊部任要條件之一：左邊要過0.21
                            if spline_dict_1["left"] <= int(GLYPH_WIDTH * 0.21):
                                is_critical_fail = True
                                if SHOW_DEBUG_MESSAGE:
                                    print("is_critical_fail left#1 occur")

                        # 如果找到了，但..., 不是想要的部份，因為筆畫太複雜，跑在中間。ex:翔
                        if spline_dict_1["left"] >= (MAP_LEFT_MIN + 0):
                            spline_fail_code = 140
                            is_add_spline = False

                # 絕對是對的。
                if spline_dict_1["left"] == glyph_margin["left"]:
                    is_add_spline = True

                # 在「絕對是對的」情況下做排除。
                if is_add_spline:
                    if use_thin_stroke_rule:
                        if spline_dict_1["right"] > (MAP_X_CENTER):
                            is_add_spline = False
                            is_critical_fail = True
                            # PS: 放棄這一個字。
                            if SHOW_DEBUG_MESSAGE:
                                print("is_critical_fail left#2 occur")


            # PS: 說明：這個設定很奇怪，因為每個字體相差很大。
            #   : 有些字體的水部超級小，例如「潤」，有些字體的水跑到幾乎正中間。
            #skip_average_mode_redical_list = '金糸魚'

            if rule_name == '右':
                #PS: 右邊比較多問題的是「錵」的「金」的點，和「翔」的「羽」，落在中間的點該算給誰？
                is_skip_average_mode = False
                if not char_radical is None:
                    if char_radical in skip_average_mode_redical_list:
                        is_skip_average_mode = True

                spline_fail_code = 200
                MAP_THRESHOLD = int(GLYPH_WIDTH * 0.32)

                # 這個值，有點難決定，因為遇到「艷」、和「枒」這2種情況是相反的。
                # PS: 也有筆劃少，但會造成 heavy 的情況，例如：及component.
                # PS: 有些字體風格習慣性讓右邊較大。例如：pop-gothic
                if use_thin_stroke_rule:
                    MAP_THRESHOLD = int(GLYPH_WIDTH * 0.38)

                if use_complex_stroke_rule:
                    # 筆劃較多
                    MAP_THRESHOLD = int(GLYPH_WIDTH * 0.29)

                if SHOW_DEBUG_MESSAGE:
                    print('MAP_THRESHOLD:', MAP_THRESHOLD)

                if spline_dict_1["left"] >= (MAP_THRESHOLD - 0):
                    is_add_spline = True

                # or
                # right must more the this limit.
                #MAP_RIGHT_MIN = int(GLYPH_WIDTH * 0.4)
                # 例外：允許超過 threshold 的，但重心在左邊。
                if not is_add_spline:
                    if not is_skip_average_mode:
                        if spline_dict_1["average_x"] >= (MAP_THRESHOLD):
                            is_add_spline = True

                            if is_add_spline:
                                FAIL_THRESHOLD = int(GLYPH_WIDTH * 0.23)
                                # 如果找到了，但..., 連在一起了. 
                                if spline_dict_1["left"] <= (FAIL_THRESHOLD):
                                    is_add_spline = False

                                    # 右邊部任要條件之一：右邊要過半
                                    # 這個可能會造成誤判：例如：錵/翔 之類的字。
                                    if spline_dict_1["right"] >= int(GLYPH_WIDTH * 0.45):
                                        is_critical_fail = True
                                        # PS: 目前這一個 is_critical_fail, 誤判率很高。
                                        if SHOW_DEBUG_MESSAGE:
                                            print("is_critical_fail right#1 occur!")
                                            print("avg:", spline_dict_1["average_x"])
                                            print("left:", spline_dict_1["left"])
                                            print("right:", spline_dict_1["right"])

                        # 如果找到了，但..., 不是想要的部份，因為筆畫太複雜，跑在中間。
                        # PS: 暫時還沒看到case.
                        #if spline_dict_1["right"] <= (MAP_RIGHT_MIN + 0):
                            #is_add_spline = False

                # 絕對是對的。
                if spline_dict_1["right"] == glyph_margin["right"]:
                    is_add_spline = True

                # 在「絕對是對的」情況下做排除。
                if is_add_spline:
                    if use_thin_stroke_rule:
                        if spline_dict_1["left"] < (MAP_X_CENTER - MAP_X_CENTER*0.1):
                            is_add_spline = False
                            is_critical_fail = True
                            # PS: 放棄這一個字。
                            if SHOW_DEBUG_MESSAGE:
                                print("is_critical_fail right#2 occur")

            # ==============================
            # 第2組合, ex: 雯
            # ==============================
            is_thin_top = False
            THIN_TOP_LIST = '艹𥫗'
            if component in THIN_TOP_LIST:
                is_thin_top = True

            is_heavy_top = False
            HEAVY_TOP_LIST = '髟鄉敖殸龍馬強保余'
            if component in HEAVY_TOP_LIST:
                is_heavy_top = True
            if strokes_total >= 10:
                is_heavy_top = True

            HEAVY_TOP_REDICAL = '土火石'
            if not char_radical is None:
                if char_radical in HEAVY_TOP_REDICAL:
                    is_heavy_top = True

            if rule_name == '上':
                spline_fail_code = 300

                MAP_THRESHOLD = int((GLYPH_WIDTH * 0.6)+ GLYPH_UNDERLINE)
                if is_thin_top:
                    MAP_THRESHOLD = int((GLYPH_WIDTH * 0.7)+ GLYPH_UNDERLINE)

                if is_heavy_top:
                    MAP_THRESHOLD = int((GLYPH_WIDTH * 0.5)+ GLYPH_UNDERLINE)

                if spline_dict_1["bottom"] >= (MAP_THRESHOLD + 0):
                    is_add_spline = True

                # or
                # 平均值在上半部
                if not is_add_spline:
                    AVERAGE_THRESHOLD = MAP_Y_CENTER
                    if is_heavy_top:
                        AVERAGE_THRESHOLD = int((GLYPH_WIDTH * 0.40)+ GLYPH_UNDERLINE)
                    FAIL_THRESHOLD = int((GLYPH_WIDTH * 0.30)+ GLYPH_UNDERLINE)

                    if SHOW_DEBUG_MESSAGE:
                        print("AVERAGE_THRESHOLD:", AVERAGE_THRESHOLD)
                        print("average_y", spline_dict_1["average_y"])
                        print("FAIL_THRESHOLD", FAIL_THRESHOLD)
                        print("bottom", spline_dict_1["bottom"])

                    if spline_dict_1["average_y"] >= (AVERAGE_THRESHOLD):
                        is_add_spline = True
                        
                        # 如果找到了，但..., 連在一起了，或太低 
                        if spline_dict_1["bottom"] <= (FAIL_THRESHOLD + 0):
                            is_add_spline = False

                # 絕對是對的。
                if spline_dict_1["top"] == glyph_margin["top"]:
                    is_add_spline = True

                # 可能是對的。
                MAP_TOP_THRESHOLD = int((GLYPH_WIDTH * 0.9)+ GLYPH_UNDERLINE)
                if spline_dict_1["top"] >= MAP_TOP_THRESHOLD:
                    is_add_spline = True

                # 在「絕對是對的」情況下做排除。
                if is_add_spline:
                    if is_thin_top:
                        if spline_dict_1["bottom"] <= (MAP_Y_CENTER + 0):
                            is_add_spline = False
                            is_critical_fail = True
                            # PS: 放棄這一個字。
                            if SHOW_DEBUG_MESSAGE:
                                print("is_critical_fail occur")


            is_heavy_bottom = False
            HEAVY_BOTTOM_LIST = '言食胡留胡須松㹜糸米龍馬鬲累鳥魚登角龜革車光勇男西酉侖俞同良艮施坐呆風約倩情專'
            HEAVY_BOTTOM_LIST += '句棗多亘宣安均作沈沐決坎事疌香卷則唐羔務逐真見親㠯卑高亢完令今彖貴要前條欶龠邑'
            HEAVY_BOTTOM_LIST += '冗圭行爾'
            
            if component in HEAVY_BOTTOM_LIST:
                is_heavy_bottom = True
            if strokes_total >= 10:
                is_heavy_bottom = True

            HEAVY_BOTTOM_REDICAL = '艸雨竹'
            if not char_radical is None:
                if char_radical in HEAVY_BOTTOM_REDICAL:
                    is_heavy_bottom = True

            if rule_name == '下':
                spline_fail_code = 400
                MAP_THRESHOLD = int((GLYPH_WIDTH * 0.4)+ GLYPH_UNDERLINE)
                if is_heavy_bottom:
                    MAP_THRESHOLD = int((GLYPH_WIDTH * 0.5)+ GLYPH_UNDERLINE)

                if spline_dict_1["top"] <= (MAP_THRESHOLD):
                    is_add_spline = True

                # or
                # 平均值在下半部
                if not is_add_spline:
                    AVERAGE_THRESHOLD = MAP_Y_CENTER
                    if is_heavy_bottom:
                        # 附註：「蔂」的累，可能有部份元件會選取不到，
                        #       為了選到上方的「田」，會造成其他字的多選，例如「餈」的次會被選到。
                        AVERAGE_THRESHOLD = int((GLYPH_WIDTH * 0.63)+ GLYPH_UNDERLINE)
                    FAIL_THRESHOLD = int((GLYPH_WIDTH * 0.70)+ GLYPH_UNDERLINE)

                    if SHOW_DEBUG_MESSAGE:
                        print("AVERAGE_THRESHOLD:", AVERAGE_THRESHOLD)
                        print("average_y", spline_dict_1["average_y"])
                        print("FAIL_THRESHOLD", FAIL_THRESHOLD)
                        print("top", spline_dict_1["top"])

                    if spline_dict_1["average_y"] <= (AVERAGE_THRESHOLD):
                        is_add_spline = True
                        
                        # 如果找到了，但..., 連在一起了，或太高
                        if spline_dict_1["top"] >= (FAIL_THRESHOLD + 0):
                            is_add_spline = False

                # 絕對是對的。
                if spline_dict_1["bottom"] == glyph_margin["bottom"]:
                    is_add_spline = True

                # 可能是對的。
                MAP_BOTTOM_THRESHOLD = int((GLYPH_WIDTH * 0.10)+ GLYPH_UNDERLINE)
                if spline_dict_1["bottom"] <= MAP_BOTTOM_THRESHOLD:
                    is_add_spline = True

            LONG_REDICAL_LENGTH = int(GLYPH_WIDTH * 0.55)
            # ==============================
            # 第3組合, ex: 運 巡
            # ==============================
            if rule_name == '左下':
                spline_fail_code = 500
                # default add all
                is_add_spline = True

                MAP_THRESHOLD = int(GLYPH_WIDTH * 0.4)

                if spline_dict_1["left"] >= (MAP_THRESHOLD - 0):
                    is_add_spline = False

                # 左下角的長邊，加入。
                if spline_dict_1["bottom"] < (MAP_Y_CENTER):
                    if spline_dict_1["left"] < (MAP_X_CENTER):
                        if (spline_dict_1["right"] - spline_dict_1["left"]) >= LONG_REDICAL_LENGTH:
                            is_add_spline = True
                            # 排除右上角的「或」
                            if spline_dict_1["average_y"] >= (MAP_Y_CENTER):
                                if spline_dict_1["average_x"] >= (MAP_X_CENTER):
                                    is_add_spline = False

                # 長到右上角的項目，刪除。
                if (spline_dict_1["right"] - spline_dict_1["left"]) < LONG_REDICAL_LENGTH:
                    if spline_dict_1["top"] > (MAP_Y_CENTER):
                        if spline_dict_1["right"] > (MAP_X_CENTER):
                            is_add_spline = False

                # 絕對是對的。
                if spline_dict_1["left"] == glyph_margin["left"]:
                    is_add_spline = True

                # 絕對是對的。
                if spline_dict_1["bottom"] == glyph_margin["bottom"]:
                    is_add_spline = True

                # 可能是對的。
                MAP_LEFT_THRESHOLD = int(GLYPH_WIDTH * 0.10)
                if spline_dict_1["left"] <= MAP_LEFT_THRESHOLD:
                    is_add_spline = True

            if rule_name == '右上':
                spline_fail_code = 600
                MAP_THRESHOLD = int(GLYPH_WIDTH * 0.24)

                if spline_dict_1["left"] >= (MAP_THRESHOLD - 0):
                    is_add_spline = True

                # 左下角的長邊，排除。
                if spline_dict_1["bottom"] < (MAP_Y_CENTER):
                    if spline_dict_1["left"] < (MAP_X_CENTER):
                        if (spline_dict_1["right"] - spline_dict_1["left"]) >= LONG_REDICAL_LENGTH:
                            is_add_spline = False


            # ==============================
            # 第4組合, ex: 屁
            # ==============================
            if rule_name == '左上':
                spline_fail_code = 700
                MAP_THRESHOLD = int(GLYPH_WIDTH * 0.2)
                MAP_THRESHOLD_LOSS = int(GLYPH_WIDTH * 0.35)

                if spline_dict_1["left"] <= (MAP_THRESHOLD - 0):
                    is_add_spline = True

                if spline_dict_1["bottom"] >= (GLYPH_WIDTH - MAP_THRESHOLD)+ GLYPH_UNDERLINE:
                    is_add_spline = True

                # 元件都在上半部，重心在略上，加入。
                if spline_dict_1["bottom"] >= MAP_Y_CENTER:
                    if spline_dict_1["average_y"] >= (GLYPH_WIDTH - MAP_THRESHOLD_LOSS)+ GLYPH_UNDERLINE:
                        is_add_spline = True

                # 元件都在左半部，重心在略左，加入。
                if spline_dict_1["right"] <= MAP_X_CENTER:
                    if spline_dict_1["average_x"] <= MAP_THRESHOLD_LOSS:
                        is_add_spline = True

                # 左側的長邊，加入。
                # PS: 這個會造成「誤加」的情況。
                if (spline_dict_1["top"] - spline_dict_1["bottom"]) >= LONG_REDICAL_LENGTH:
                    if spline_dict_1["average_x"] < (MAP_X_CENTER):
                        is_add_spline = True
                    else:
                        is_add_spline = False

                # 重心在極左上，加入。
                if spline_dict_1["average_y"] >= (GLYPH_WIDTH - MAP_THRESHOLD)+ GLYPH_UNDERLINE:
                    if spline_dict_1["average_x"] <= (MAP_THRESHOLD):
                        is_add_spline = True

                # 重心：右下，排除。
                if spline_dict_1["average_y"] <= (MAP_Y_CENTER):
                    if spline_dict_1["average_x"] >= (MAP_X_CENTER):
                        is_add_spline = False

                # 絕對是對的。
                if spline_dict_1["left"] == glyph_margin["left"]:
                    is_add_spline = True

                # 絕對是對的。
                if spline_dict_1["top"] == glyph_margin["top"]:
                    is_add_spline = True

                # 可能是對的。
                MAP_LEFT_THRESHOLD = int(GLYPH_WIDTH * 0.10)
                if spline_dict_1["left"] <= MAP_LEFT_THRESHOLD:
                    is_add_spline = True

            if rule_name == '右下':
                spline_fail_code = 800
                # default add all

                MAP_THRESHOLD = int(GLYPH_WIDTH * 0.2)
                MAP_THRESHOLD_LOSS = int(GLYPH_WIDTH * 0.3)

                if spline_dict_1["left"] >= (MAP_THRESHOLD - 0):
                    if spline_dict_1["top"] <= (GLYPH_WIDTH - MAP_THRESHOLD)+ GLYPH_UNDERLINE:
                        is_add_spline = True

                # 元件都在上半部，重心在略上，排除。
                if spline_dict_1["bottom"] >= MAP_Y_CENTER:
                    if spline_dict_1["average_y"] >= (GLYPH_WIDTH - MAP_THRESHOLD_LOSS)+ GLYPH_UNDERLINE:
                        is_add_spline = False


                # 元件都在左半部，重心在略左，排除。
                # PS: 這個可能會排除「屁」的第一個比。
                if spline_dict_1["right"] <= MAP_X_CENTER:
                    if spline_dict_1["average_x"] <= MAP_THRESHOLD_LOSS:
                        is_add_spline = False

                # 左側的長邊，排除。
                if (spline_dict_1["top"] - spline_dict_1["bottom"]) >= LONG_REDICAL_LENGTH:
                    if spline_dict_1["average_x"] < (MAP_X_CENTER):
                        is_add_spline = False
                    else:
                        is_add_spline = True

                # 重心在極左上，排除。
                if spline_dict_1["average_y"] >= (GLYPH_WIDTH - MAP_THRESHOLD)+ GLYPH_UNDERLINE:
                    if spline_dict_1["average_x"] <= (MAP_THRESHOLD):
                        is_add_spline = False

                # 重心：右下，加入。
                if spline_dict_1["average_y"] <= (MAP_Y_CENTER):
                    if spline_dict_1["average_x"] >= (MAP_X_CENTER):
                        is_add_spline = True

                # 絕對是，排除的。
                if spline_dict_1["left"] == glyph_margin["left"]:
                    is_add_spline = False

                # 絕對是，排除的。
                if spline_dict_1["top"] == glyph_margin["top"]:
                    is_add_spline = False


            # ==============================
            # 例外組合1
            # ==============================
            if rule_name == '全':
                is_add_spline = True

            # time to say goodbye.
            if is_critical_fail:
                is_found_component = False
                break

            if not is_add_spline:
                if SHOW_DEBUG_MESSAGE:
                    print("spline fail, rule:%s, code:%d" % (rule_name, spline_fail_code) )
                pass
            else:
                if SHOW_DEBUG_MESSAGE:
                    print("spline bingo!")
                new_key_index = len(intersection_dict)+1
                intersection_dict[new_key_index]=spline_dict_1.copy()
                is_found_component = True


    return is_found_component, intersection_dict

def new_glyph_file(output_folder, unicode_int, glyph_width, file_index=1):
    SHOW_DEBUG_MESSAGE = False  # online
    #SHOW_DEBUG_MESSAGE = True   # debug

    unicode_hex = str(hex(unicode_int))[2:].upper()
    filename = "uni%s.glyph" % (unicode_hex)
    output_filepath = join(output_folder, filename)

    # conflict
    if exists(output_filepath):
        for idx in range(10000):
            filename = "uni%s_%d.glyph" % (unicode_hex,idx)
            output_filepath = join(output_folder, filename)
            if not exists(output_filepath):
                break

    if SHOW_DEBUG_MESSAGE:
        print("save to filepath:", output_filepath)

    output_file = open(output_filepath, 'w')


    new_glyph = '''StartChar: uni%s
Encoding: %s %s %d
Width: %d
Flags: W
LayerCount: 2
Fore
SplineSet
EndSplineSet
EndChar''' % (unicode_hex, unicode_int, unicode_int, file_index, glyph_width)

    output_file.write(new_glyph)
    output_file.close()

    return output_filepath

def component_from_rule(parse_char, dict_data, rule_name, component, filename_input_1, UNICODE_FIELD, GLYPH_WIDTH, GLYPH_UNDERLINE, output_folder, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_DEBUG_MESSAGE):
    #SHOW_DEBUG_MESSAGE = False  # online
    #SHOW_DEBUG_MESSAGE = True   # debug

    ret = False
    glyph_filepath = None

    unicode_int = ord(component)

    stroke_dict_1, unicode_int_1 = get_stroke_dict(filename_input_1, UNICODE_FIELD)

    if SHOW_DEBUG_MESSAGE:
        print("process unicodes: %d" % (unicode_int_1))

    glyph_margin = compute_stroke_margin(stroke_dict_1)

    is_found_component, new_stroke_dict = get_component(parse_char, dict_data, stroke_dict_1, glyph_margin, component, rule_name, GLYPH_WIDTH, GLYPH_UNDERLINE, THIN_COMPONENT, HEAVY_COMPONENT, skip_average_mode_redical_list, SHOW_DEBUG_MESSAGE)

    if is_found_component:
        glyph_filepath = new_glyph_file(output_folder, unicode_int, GLYPH_WIDTH)
        write_to_file(glyph_filepath, new_stroke_dict)
        ret = True

    return ret, glyph_filepath

def compare_intersection(component, filename_input_1, filename_input_2, UNICODE_FIELD, GLYPH_WIDTH, output_folder):
    ret = False
    glyph_filepath = None

    unicode_int = ord(component)

    stroke_dict_1, unicode_int_1 = get_stroke_dict(filename_input_1, UNICODE_FIELD)
    stroke_dict_2, unicode_int_2 = get_stroke_dict(filename_input_2, UNICODE_FIELD)

    print("compare unicodes: %d - %d" % (unicode_int_1,unicode_int_2))

    glyph_margin_1 = compute_stroke_margin(stroke_dict_1)
    glyph_margin_2 = compute_stroke_margin(stroke_dict_2)
    is_found_component, new_stroke_dict = get_intersection(stroke_dict_1, stroke_dict_2)

    if is_found_component:
        glyph_filepath = new_glyph_file(output_folder, unicode_int, GLYPH_WIDTH)
        write_to_file(glyph_filepath, new_stroke_dict)
        ret = True

    return ret, glyph_filepath

def cli():
    UNICODE_FIELD = 2

    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--input1",
        help="input glyph file1",
        required=True,
        type=str)

    parser.add_argument("--input2",
        help="input glyph file2",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        type=str)

    args = parser.parse_args()

    GLYPH_WIDTH = 1024
    # hard code here.
    component = '犭'
    output_folder = args.output
    filename_input_1, filename_input_2 = args.input1, args.input2
    intersection_result, glyph_filepath = compare_intersection(component, filename_input_1, filename_input_2, UNICODE_FIELD, GLYPH_WIDTH, output_folder)

if __name__ == "__main__":
    cli()
