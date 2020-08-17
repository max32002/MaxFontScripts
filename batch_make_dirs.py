#!/usr/bin/env python3
#encoding=utf-8

#find ./swei-* -name "*.ttf"
ttf_list = [
'bmp-noto-leg-Black'
,'bmp-noto-leg-Bold'
,'bmp-noto-leg-DemiLight'
,'bmp-noto-leg-Light'
,'bmp-noto-leg-Medium'
,'bmp-noto-leg-Regular'
,'bmp-noto-leg-Thin'
,'bmp-swei-sans-Black'
,'bmp-swei-sans-Bold'
,'bmp-swei-sans-DemiLight'
,'bmp-swei-sans-Light'
,'bmp-swei-sans-Medium'
,'bmp-swei-sans-Regular'
,'bmp-swei-sans-Thin'
]

for item in ttf_list:
	item = item.replace(' ','\\ ')
	for idx in range(9):
		cmd = "mkdir %s/%d" % (item,idx+1)
		print(cmd)

		cmd = "mv %s/U_%d* %s/%d" % (item, idx+1, item, idx+1)
		print(cmd)

		cmd = "find %s/ -maxdepth 1 -name \"U_%d*\" -exec mv {} %s/%d \\;" % (item, idx+1, item, idx+1)
		print(cmd)
