#!/usr/bin/env python3
#encoding=utf-8

import argparse

def get_word_set(file_path):
    input_file = open(file_path, 'r')

    my_set = set()

    stop_words = "(){} /\\-_"
    idx = 1
    for x_line in input_file:
        is_my_line = True
        
        if is_my_line:
            new_line = x_line
            #utput_file.write(new_line)
            for char in new_line:
                if char in stop_words:
                    continue
                if not char in my_set:
                    my_set.add(ord(char))

    input_file.close()

    #my_set = sorted(my_set)
    return my_set

def output_to_file(filename_output, myfont_set):
    my_set = sorted(myfont_set)
    print("result to file:", filename_output)
    outfile = open(filename_output, 'w')

    for item in my_set:
        try:
            #output_string = "%s(%s)" % (chr(item),str(hex(item))[2:])
            output_string = "%s" % (chr(item))
        except Exception as exc:
            print("error item:%d" %(item))
            print("error item(hex):%s" %(str(hex(item))))
            raise
            #pass
        outfile.write(output_string)
    outfile.close()

def copy_out(args):
    more_ff, less_ff = args.more, args.less
    mode = args.mode
    output_filename = args.output

    is_output_result = True  # get real file.

    # start to scan files.
    print("more filename:", more_ff)
    print("less filename:", less_ff)
    print("mode:", mode)
    print("output filename:", output_filename)

    more_unicode_set = get_word_set(more_ff)
    less_unicode_set = get_word_set(less_ff)
    
    diff_set_more =  less_unicode_set - more_unicode_set
    diff_set_lost =  more_unicode_set - less_unicode_set
    diff_set_common =  more_unicode_set & less_unicode_set

    print("length more text:", len(more_unicode_set))
    print("length less text:", len(less_unicode_set))
    print("length less - more:", len(diff_set_more))
    print("length more - less (will be copy out):", len(diff_set_lost))
    print("length intersection:", len(diff_set_common))

    if is_output_result:
        target_set = ()
        
        # copy lost out.
        if mode == "lost":
            target_set = diff_set_lost

        # copy intersection out.
        #if mode == "intersection":
        if mode[:1] == "i":
            target_set = diff_set_common

        # copy more out.
        if mode == "more":
            target_set = diff_set_more

        output_to_file(output_filename,target_set)

def cli():
    parser = argparse.ArgumentParser(
            description="compare two text filename")

    parser.add_argument("--more",
        help="more text filename",
        required=True,
        type=str)

    parser.add_argument("--less",
        help="less text filename",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output compare result",
        default='compare.txt',
        type=str)

    parser.add_argument("--mode",
        help="selected string",
        default='lost',
        type=str)

    args = parser.parse_args()
    copy_out(args)

if __name__ == "__main__":
    cli()
