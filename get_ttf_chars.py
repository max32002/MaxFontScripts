#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os.path import join, exists, normpath, basename


def output_to_file(myfile, myfont_set):
    for item in myfont_set:
        # filter
        if item < 13300:
            #continue
            pass
        
        if item > 65000:
            #continue
            pass
        
        try:
            #output_string = "%s(%s)" % (chr(item),str(hex(item))[2:])
            output_string = "%s" % (chr(item))
            #output_string = "%s\n" % (chr(item))
            #output_string = "%s " % (chr(item))
            #output_string = '"%s",' % (chr(item))
        except Exception as exc:
            print("error item:%d" %(item))
            print("error item(hex):%s" %(str(hex(item))))
            raise
            #pass
        myfile.write(output_string)


def get_ttf_chars_list(source_ff, unicode_field):
    #source_ff = 'Naikai_yue.sfdir'
    source_unicode_set, source_dict = LibGlyph.load_files_to_set_dict(source_ff, unicode_field)

    print("length source:", len(source_unicode_set))
    print("output compare result to file...")

    filename_output = "ttf_char_list_%s.txt" % (basename(normpath(source_ff)))
    print("output file: %s" % filename_output)
    outfile = open(filename_output, 'w')
    sorted_set=sorted(source_unicode_set)
    output_to_file(outfile,sorted_set)
    outfile.close()


if __name__ == '__main__':
    import sys

    # from 1 to 3.
    #unicode_field = 2       # for Noto Sans
    unicode_field = 2

    argument_count = 1 + 1
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[1]
        if len(source_ff) > 1:
            if not ".sfdir" in source_ff:
                source_ff += ".sfdir"
            get_ttf_chars_list(source_ff, unicode_field)
            
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))

