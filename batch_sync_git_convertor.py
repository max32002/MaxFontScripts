#!/usr/bin/env python3
#encoding=utf-8

#find ./swei-* -name "*.ttf"
ttf_list = [
'~/Documents/git/max-hana/'
,'~/Documents/git/swei-d-lucy/'
,'~/Documents/git/swei-gothic/'
,'~/Documents/git/swei-halfmoon/'
,'~/Documents/git/swei-meatball/'
,'~/Documents/git/swei-sans/'
,'~/Documents/git/swei-spring/'
,'~/Documents/git/swei-b2-leg/'
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
,'~/Documents/git/swei-del-luna-sans/'
,'~/Documents/git/swei-gospel-sans/'
,'~/Documents/git/swei-shear-sans/'
,'~/Documents/git/swei-spike-sans/'
,'~/Documents/git/swei-alias-sans/'
,'~/Documents/git/swei-fist-sans/'
,'~/Documents/git/swei-marker-sans/'
,'~/Documents/git/swei-devil-sans/'
,'~/Documents/git/swei-bell-sans/'
,'~/Documents/git/swei-ax-sans/'
,'~/Documents/git/swei-bone-sans/'
,'~/Documents/git/swei-match-sans/'
,'~/Documents/git/swei-dart-sans/'
]

# TODO:
# ,'~/Documents/git/nanifont/'

for item in ttf_list:
	item = item.replace(' ','\\ ')
	cmd = "cd %s" % (item)
	print(cmd)

	cmd = "git add python"
	print(cmd)

	cmd = "git commit -m \"ver 2.130 convertor\""
	print(cmd)

	cmd = "git push"
	print(cmd)
