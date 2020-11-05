#!/usr/bin/env python3
#encoding=utf-8

#find ./swei-* -name "*.ttf"
ttf_list = [
'swei-b2-leg'
,'swei-b2-sans'
,'swei-b2-serif'
,'swei-d-lucy'
,'swei-gothic'
,'swei-halfmoon'
,'swei-meatball'
,'swei-sans'
,'swei-spring'
,'swei-xd'
]

for item in ttf_list:
	item = item.replace(' ','\\ ')
	cmd = "mkdir %s/WebFont" % (item)
	print(cmd)
	cmd = "mkdir %s/WebFont/CJK\\ TC" % (item)
	print(cmd)
	cmd = "mkdir %s/WebFont/CJK\\ SC" % (item)
	print(cmd)
	cmd = "mkdir %s/WebFont/CJK\\ JP" % (item)
	print(cmd)


