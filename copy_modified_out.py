#!/usr/bin/env python3
#encoding=utf-8

from os import listdir, remove, rename, stat, makedirs
from os.path import join, exists, splitext

# to copy/move file.
import shutil

import time
from datetime import datetime

def scan_files(ff_folder, target_folder, last_modified_time):
    files = listdir(ff_folder)
    file_count = 0
    copy_count = 0
    
    datetime_object = datetime.strptime(last_modified_time, '%Y-%m-%d %H:%M:%S')
    print("Scaning folder:", ff_folder , "\nCopy to:", target_folder)
    print("Last modified time:", last_modified_time)
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
                
            source_path = join(ff_folder,f)

            match_interval = False

            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = stat(source_path)
            #print("last modified: %s" % time.ctime(mtime))
            #print("last modified: %s" % mtime)
            #current_time = datetime.datetime.now().time()
            #time_diff = current_time - mtime
            #print("time_diff:", time_diff)
            #current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            #print("current_time:", current_time)
            #print("current_time:", time.time())

            #time_diff = time.time() - mtime
            target_time = datetime.timestamp(datetime_object)
            time_diff = target_time - mtime
            
            time_diff_min = int(time_diff / 60)
            #print("time_diff sec:", time_diff)
            #print("time_diff min:", time_diff_min)
            #print("time_diff hour:", int((time_diff / 60)/60))

            if mtime >= target_time:
                match_interval = True

            if match_interval:
                #print("match filepath:", source_path)
                target_path = join(target_folder,f)
                shutil.copy(source_path,target_path)
                copy_count += 1

    print("file_count:", file_count)
    print("copy_count:", copy_count)


if __name__ == '__main__':

    import sys
    argument_count = 4

    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        target_folder = sys.argv[2]
        last_modified_time = sys.argv[3]
        if len(source_ff) > 0:
            if not exists(target_folder):
                makedirs(target_folder)
                print("Directory " , target_folder ,  " Created ") 

            if not exists(source_ff):
                if not ".sfdir" in source_ff:
                    source_ff += ".sfdir"
            if exists(source_ff):
                scan_files(source_ff, target_folder, last_modified_time)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s ff_folder target_folder last_modified_time" % (sys.argv[0]))
