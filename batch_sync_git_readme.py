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
,'~/Documents/git/swei-gospel-leg/'
,'~/Documents/git/swei-shear-sans/'
,'~/Documents/git/swei-shear-leg/'
,'~/Documents/git/swei-spike-sans/'
,'~/Documents/git/swei-spike-leg/'
,'~/Documents/git/swei-alias-sans/'
,'~/Documents/git/swei-alias-leg/'
,'~/Documents/git/swei-fist-sans/'
,'~/Documents/git/swei-fist-leg/'
,'~/Documents/git/swei-marker-sans/'
,'~/Documents/git/swei-marker-leg/'
,'~/Documents/git/swei-sugar/'
,'~/Documents/git/swei-b2-sugar/'
,'~/Documents/git/swei-devil-sans/'
,'~/Documents/git/swei-devil-leg/'
,'~/Documents/git/swei-bell-sans/'
,'~/Documents/git/swei-bell-leg/'
,'~/Documents/git/swei-ax-sans/'
,'~/Documents/git/swei-ax-leg/'
,'~/Documents/git/swei-bone-sans/'
,'~/Documents/git/swei-bone-leg/'
,'~/Documents/git/swei-match-sans/'
,'~/Documents/git/swei-match-leg/'
,'~/Documents/git/swei-dart-sans/'
,'~/Documents/git/swei-dart-leg/'
,'~/Documents/git/swei-fan-sans/'
,'~/Documents/git/swei-fan-leg/'
,'~/Documents/git/swei-fan-serif/'
,'~/Documents/git/swei-jay-sans/'
,'~/Documents/git/swei-jay-leg/'
,'~/Documents/git/swei-jay-serif/'
,'~/Documents/git/kurewa-gothic/'
,'~/Documents/git/maruko-gothic/'
,'~/Documents/git/swei-right-bottom-sans/'
,'~/Documents/git/swei-right-bottom-leg/'
]

# TODO:
# 



for item in ttf_list:
	item = item.replace(' ','\\ ')
	reuse_file = '~/Documents/sh/fix_git_readme_urls/README.md'
	
	if item[:1]=="~":
		item = os.path.expanduser(item)

	if reuse_file[:1]=="~":
		reuse_file = os.path.expanduser(reuse_file)

	begin_string = "## 相關網頁"
	#begin_string = "    * 可自由改作為其他字型 將字型檔案修改重製為其他字型檔案，改作後的字型檔案須同樣依 Open Font License 釋出。"
	resume_string = "https://max-everyday.com/about/#donate"
	cmd = "~/Documents/sh/update_block_from_file.py --first \"%sREADME.md\"" % (item.replace("\"","\\\""))
	cmd += " --second \"%s\"" % (reuse_file.replace("\"","\\\""))
	cmd += " --begin \"%s\"" % (begin_string.replace("\"","\\\""))
	cmd += " --resume \"%s\"" % (resume_string.replace("\"","\\\""))
	print(cmd)
