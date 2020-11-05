#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import makedirs
from os.path import join, exists, normpath, basename

# to copy file.
import shutil

import argparse

import GlyphCompare

def preview(target_ff):
    if not "/" in target_ff:
        target_ff = abspath(target_ff)
    cmd = "/Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge " + target_ff
    process = subprocess.Popen(cmd, shell=True)

def output_to_file(myfile, myfont_set):
    for item in myfont_set:
        try:
            #output_string = "%s(%s)" % (chr(item),str(hex(item))[2:])
            output_string = "%s" % (chr(item))
        except Exception as exc:
            print("error item:%d" %(item))
            print("error item(hex):%s" %(str(hex(item))))
            raise
            #pass
        myfile.write(output_string)


def do_resize(args):
    more_ff, less_ff = args.more, args.less

    is_output_to_file = True    # debug
    if args.log != "True":
        is_output_to_file = False   # online

    upgrade_folder = args.output

    # from 1 to 3.
    #unicode_field = 2       # for Noto Sans
    unicode_field = args.unicode_field

    show_debug_message = True
    show_debug_message = False      # online
    
    # start to scan files.
    print("more project:", more_ff)
    print("less project:", less_ff)

    source_unicode_set, source_dict = LibGlyph.load_files_to_set_dict(more_ff, unicode_field)
    target_unicode_set, target_dict = LibGlyph.load_files_to_set_dict(less_ff, unicode_field)

    diff_set_more =  target_unicode_set - source_unicode_set
    diff_set_lost =  source_unicode_set - target_unicode_set
    diff_set_common =  source_unicode_set & target_unicode_set

    print("length more project:", len(source_unicode_set))
    print("length less project:", len(target_unicode_set))
    print("length less - more:", len(diff_set_more))
    print("length more - less (will be copy out):", len(diff_set_lost))
    print("length intersection:", len(diff_set_common))

    if is_output_to_file:
        filename_output = "resize_%s.log" % (basename(normpath(less_ff)))
        print("compare result to file:", filename_output)

        outfile = open(filename_output, 'w')
        sorted_set=sorted(diff_set_lost)
        output_to_file(outfile,sorted_set)
        outfile.close()


    # start to compare common part.
    compare_count = 0
    resize_count = 0
    for item in diff_set_common:
        compare_count += 1

        source_path = join(more_ff,source_dict[item])
        target_path = join(less_ff,target_dict[item])
        
        stroke_dict_source, unicode_int_source = GlyphCompare.get_stroke_dict(source_path, unicode_field)
        glyph_margin_source = GlyphCompare.compute_stroke_margin(stroke_dict_source)

        stroke_dict_target, unicode_int_target = GlyphCompare.get_stroke_dict(target_path, unicode_field)
        glyph_margin_target = GlyphCompare.compute_stroke_margin(stroke_dict_target)
        
        if show_debug_message:
            print("source_path:", source_path)
            print("target_path:", target_path)
            print("source glyph_margin:", glyph_margin_source)
            print("target glyph_margin:", glyph_margin_target)

        bottom_diff = 0

        #PS: 使用 1會有問題，建議使用最少的腳長度。
        min_remove_leg_length = 3

        if (not glyph_margin_target["bottom"] is None) and (not glyph_margin_source["bottom"] is None):
            bottom_diff = glyph_margin_target["bottom"] - glyph_margin_source["bottom"]

            #PS: 使用 1會有問題，建議使用最少的腳長度。
            if bottom_diff > min_remove_leg_length:
                if (not glyph_margin_target["top"] is None) and (not glyph_margin_source["top"] is None):
                    if glyph_margin_target["top"] != glyph_margin_source["top"]:
                        # error occur! maybe is source font not correct.
                        bottom_diff = 0

                if (not glyph_margin_target["left"] is None) and (not glyph_margin_source["left"] is None):
                    if glyph_margin_target["left"] != glyph_margin_source["left"]:
                        # error occur! maybe is source font not correct.
                        bottom_diff = 0

                if (not glyph_margin_target["right"] is None) and (not glyph_margin_source["right"] is None):
                    if glyph_margin_target["right"] != glyph_margin_source["right"]:
                        # error occur! maybe is source font not correct.
                        bottom_diff = 0


        # due to int() may lost 1.
        #PS: 使用 1會有問題，建議使用最少的腳長度。
        if bottom_diff > min_remove_leg_length:
            height_source = glyph_margin_source["top"] - glyph_margin_source["bottom"]
            height_target = glyph_margin_target["top"] - glyph_margin_target["bottom"]
            resize_percent = height_source / height_target

            # move to center
            new_transform_cmd = ['MOVE','','Y',-1 * int(bottom_diff/2)]
            GlyphCompare.transform_stroke(stroke_dict_target,new_transform_cmd)

            new_transform_cmd = ['SCALE','','XY', resize_percent]
            GlyphCompare.transform_stroke(stroke_dict_target,new_transform_cmd)

            resize_count += 1

            glyph_margin_target = GlyphCompare.compute_stroke_margin(stroke_dict_target)
            if show_debug_message:
                print("Char:", chr(item))
                print("after target glyph_margin:", glyph_margin_target)

            GlyphCompare.write_to_file(target_path, stroke_dict_target)

    print("compare count:", compare_count)
    print("resize count:", resize_count)

    if args.preview == "True":
        preview(less_ff)

def cli():
    parser = argparse.ArgumentParser(
            description="Converts fonts using FontForge")

    parser.add_argument("--more",
        help="input more glyph font sfdir folder",
        required=True,
        type=str)

    parser.add_argument("--less",
        help="output less glyph font sfdir folder",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output glyth folder",
        default='lost.sfdir',
        type=str)

    parser.add_argument("--unicode_field",
        help="unicode_field in glyth",
        default=2,
        type=int)

    parser.add_argument("--log",
        help="generate log file",
        default="False",
        type=str)

    parser.add_argument("--preview",
        help="user ff to preview",
        default='False',
        type=str)

    args = parser.parse_args()
    do_resize(args)



if __name__ == "__main__":
    cli()
