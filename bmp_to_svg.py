#!/usr/bin/env python3
#encoding=utf-8
# https://github.com/scour-project/scour
# pip install scour
import argparse
import os
import subprocess
import concurrent.futures
import platform

def main(args):
    from_folder = args.input
    to_folder = args.output
    multi_thread = True
    if args.single_thread:
        multi_thread = False

    if len(to_folder) == 0:
        to_folder = from_folder
    print("From folder:", from_folder)
    print("To folder:", to_folder)

    cmd_list = []
    idx=0
    convert_count=0
    
    filename_list = []
    target_folder_list = os.listdir(from_folder)
    print("Total file in from folder:", len(target_folder_list))
    
    working_dir = os.getcwd()
    print("Working folder:", working_dir)

    if not args.cwd is None:
        working_dir = args.cwd
        print("Assigned Working folder:", working_dir)

    for filename in target_folder_list:
        is_supported_image = False
        if filename.endswith(".bmp") or filename.endswith(".pbm") or filename.endswith(".pgm") or filename.endswith(".ppm"): 
            is_supported_image = True
        if is_supported_image:
            filename_list.append(filename)

    for filename in filename_list:
        idx+=1
        #print("convert filename:", name)
        from_svg_path = os.path.join(from_folder, filename)
        filename_main = os.path.splitext(os.path.basename(filename))[0]
        to_svg_path = os.path.join(to_folder, filename_main + ".svg")
        shell_cmd = args.potrace + ' -b svg -u 60 %s -o %s' % (from_svg_path, to_svg_path)
        #print("shell_cmd:", shell_cmd)
        
        cmd_argument = []
        cmd_argument.append('-b')
        cmd_argument.append('svg')
        cmd_argument.append('-u')
        cmd_argument.append('60')
        cmd_argument.append(from_svg_path)
        cmd_argument.append('-o')
        cmd_argument.append(to_svg_path)

        if not multi_thread:
            # single thread
            if platform.system() == 'Linux':
                cmd_array = [args.potrace] + cmd_argument
                s=subprocess.Popen(cmd_array, cwd=args.cwd)
            else:
                subprocess.call(shell_cmd, cwd=args.cwd)
                #subprocess.Popen(shell_cmd, shell=True)
        convert_count+=1

        # multi thread
        cmd_list.append(shell_cmd)
        
        if idx % 1000 == 0:
            # single thread
            #print("Processing svg: %d" % (idx))
            pass

    if multi_thread:
        # multi thread
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(subprocess.call, cmd_list)

    print("Convert file count: %d\n" % (convert_count))

def cli():
    parser = argparse.ArgumentParser(
            description="batch convert svg from source folder to target folder")

    parser.add_argument("--input",
        help="source folder",
        type=str)

    parser.add_argument("--output",
        help="target folder",
        default="", 
        type=str)

    parser.add_argument('--single_thread', action='store_true')

    parser.add_argument('--cwd', type=str)
    parser.add_argument('--potrace', type=str, default='potrace')

    
    args = parser.parse_args()

    pass_precheck = True
    
    if not os.path.exists(args.input):
        pass_precheck = False
        print("input folder not found: %s" % (args.input))

    if not os.path.exists(args.output):
        #pass_precheck = False
        #print("output folder not found: %s" % (args.output))
        if not os.path.isdir(args.output):
            os.mkdir(args.output)

    if pass_precheck:
        main(args)

if __name__ == "__main__":
    cli()
