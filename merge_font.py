#!/usr/bin/env python3
# coding=utf8

import os
import argparse

from fontTools.ttLib import TTFont
from fontTools.merge import Merger

def merge_font(font1, font2, output):
	# Merge the fonts
	merger = Merger()
	new_font = merger.merge([font1, font2])

	# Save the merged font
	new_font.save(output)

def cli():
    parser = argparse.ArgumentParser(
            description="merge font")

    parser.add_argument("--font1",
        help="input font1 file",
        required=True,
        type=str)

    parser.add_argument("--font2",
        help="input font2 file",
        required=True,
        type=str)

    parser.add_argument("--output",
        help="output font folder",
        default="output.ttf",
        type=str)

    args = parser.parse_args()

    pass_precheck = True
    
    if not os.path.exists(args.font1):
        pass_precheck = False
        print("font1 file not found: %s" % (args.font1))

    if not os.path.exists(args.font2):
        pass_precheck = False
        print("font2 file not found: %s" % (args.font2))

    if pass_precheck:
        merge_font(args.font1, args.font2, args.output)

if __name__ == "__main__":
    cli()
