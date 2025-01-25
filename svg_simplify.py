#!/usr/bin/env python3
#encoding=utf-8
# https://github.com/scour-project/scour
# pip install scour
import argparse
import os
import glob
import subprocess
import concurrent.futures

def main(args):
    from_folder = args.input
    to_folder = args.output

    # overwrite
    if len(to_folder) == 0:
        to_folder = from_folder
    print("From folder:", from_folder)
    print("To folder:", to_folder)

    cmd_list = []
    idx=0
    convert_count=0
    filename_pattern = from_folder + "/*.svg"
    for from_svg_path in glob.glob(filename_pattern):
        idx+=1
        #print("convert filename:", name)
        filename = os.path.basename(from_svg_path)
        to_svg_path = os.path.join(to_folder, filename)
        shell_cmd = 'scour -q -i %s -o %s --enable-viewboxing --enable-id-stripping --enable-comment-stripping --shorten-ids --indent=none' % (from_svg_path, to_svg_path)
        #print("shell_cmd:", shell_cmd)
        
        # single thread
        #subprocess.call(shell_cmd)
        convert_count+=1

        # multi thread
        cmd_list.append(shell_cmd)
        
        if idx % 1000 == 0:
            # single thread
            #print("Processing svg: %d" % (idx))
            pass

    # multi thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(subprocess.call, cmd_list)

    print("Convert file count:%d\n" % (convert_count))

def cli():
    parser = argparse.ArgumentParser(
            description="get ttf chars list")

    parser.add_argument("--input",
        help="source folder",
        type=str)

    parser.add_argument("--output",
        help="target folder",
        default="", 
        type=str)
    
    args = parser.parse_args()

    pass_precheck = True
    
    if not os.path.exists(args.input):
        pass_precheck = False
        print("input folder not found: %s" % (args.input))

    if not os.path.exists(args.output):
        pass_precheck = False
        print("output folder not found: %s" % (args.output))

    if pass_precheck:
        main(args)

if __name__ == "__main__":
    cli()
