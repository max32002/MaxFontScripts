#!/usr/bin/env python3
#encoding=utf-8

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
,'~/Documents/git/swei-toothpaste/'
,'~/Documents/git/swei-bat-sans/'
,'~/Documents/git/swei-bow-leg/'
,'~/Documents/git/nanifont/'
]

# TODO:
# ,

for item in ttf_list:
	item = item.replace('~/Documents/git/','')
	item = item.replace('/','')
	cmd = "git clone https://github.com/max32002/%s" % (item)
	print(cmd)
