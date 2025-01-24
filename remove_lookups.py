#!/usr/bin/env python3
# coding=utf8

import sys
import os.path

def count_lookups(f):   
    """Count lookups in font and return the lookup keys"""
    lookups = list(f.gsub_lookups) + list(f.gpos_lookups)      
    print('The font has {} lookups'.format(len(lookups)))
    return lookups

if len(sys.argv) != 2:
    sys.exit("Usage: Give one font file name as argument")
    
font = fontforge.open(sys.argv[1])

lookups = count_lookups(font)
                         
print('Removing lookup')   
#for l in lookups:
font.removeLookup(lookups[10])
                              
count_lookups(font)
                     
print('Generating \'output.ttf\'...')
font.generate('output.ttf')
font.close()

print('Opening generated font file to output2.ttf ...')
font2 = fontforge.open('output.ttf')

count_lookups(font2)

font2.generate('output2.ttf')
font2.close()
