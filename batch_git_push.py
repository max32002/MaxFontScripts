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
]

# TODO:
# ,'~/Documents/git/nanifont/'

for item in ttf_list:
	item = item.replace(' ','\\ ')
	cmd = "cd %s" % (item)
	print(cmd)

	cmd = "git add README.md"
	print(cmd)

	cmd = "git commit -m \"update related URLs\""
	print(cmd)

	cmd = "git push"
	print(cmd)
