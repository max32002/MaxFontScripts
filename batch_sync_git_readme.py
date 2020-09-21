#!/usr/bin/env python3
#encoding=utf-8

import os

#find ./swei-* -name "*.ttf"
ttf_list = [
'~/Documents/git/max-hana/'
,'~/Documents/git/bakudaifont/'
,'~/Documents/git/FakePearl/'
,'~/Documents/git/JasonHandWritingFonts/'
,'~/Documents/git/masafont/'
,'~/Documents/git/naikaifont/'
,'~/Documents/git/swei-d-lucy/'
,'~/Documents/git/swei-gothic/'
,'~/Documents/git/swei-halfmoon/'
,'~/Documents/git/swei-meatball/'
,'~/Documents/git/swei-sans/'
,'~/Documents/git/swei-spring/'
,'~/Documents/git/TaiwanPearl/'
,'~/Documents/git/YuPearl/'
,'~/Documents/git/swei-b2-leg/'
,'~/Documents/git/MaxFontScripts/'
,'~/Documents/git/swei-b2-serif/'
,'~/Documents/git/swei-b2-sans/'
,'~/Documents/git/swei-xd/'
,'~/Documents/git/swei-rainbow-leg/'
,'~/Documents/git/swei-gothic-leg/'
,'~/Documents/git/swei-nut-leg/'
,'~/Documents/git/swei-nut-sans/'
,'~/Documents/git/swei-3t-sans/'
,'~/Documents/git/swei-3t-leg/'
,'~/Documents/git/swei-toothpaste/'
,'~/Documents/git/swei-bat-sans/'
,'~/Documents/git/swei-bow-leg/'
,'~/Documents/git/swei-bow-sans/'
,'~/Documents/git/swei-curve-leg/'
,'~/Documents/git/swei-curve-sans/'
,'~/Documents/git/nanifont/'
,'~/Documents/git/swei-del-luna-sans/'
,'~/Documents/git/swei-del-luna-leg/'
,'~/Documents/git/swei-gospel-sans/'
,'~/Documents/git/swei-shear-sans/'
]

# TODO:
# 



for item in ttf_list:
	item = item.replace(' ','\\ ')
	reuse_file = '~/Documents/sh/fix_font_readme_urls/README.md'
	
	if item[:1]=="~":
		item = os.path.expanduser(item)

	if reuse_file[:1]=="~":
		reuse_file = os.path.expanduser(reuse_file)

	begin_string = "## 相關網頁"
	resume_string = "https://max-everyday.com/about/#donate"
	cmd = "~/Documents/sh/update_block_from_file.py --first \"%sREADME.md\"" % (item.replace("\"","\\\""))
	cmd += " --second \"%s\"" % (reuse_file.replace("\"","\\\""))
	cmd += " --begin \"%s\"" % (begin_string.replace("\"","\\\""))
	cmd += " --resume \"%s\"" % (resume_string.replace("\"","\\\""))
	print(cmd)
