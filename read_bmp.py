#!/usr/bin/env python3
#encoding=utf-8

from PIL import Image

def ff_x_to_bmp_x(x):
    return x + 10

def ff_y_to_bmp_y(y):
    return 880 + (y * -1)

def ff_block_sum(bmp_image, x1,y1,x2,y2):
    matrix=[]
    print("bmp coordinate x,y to x,y",ff_x_to_bmp_x(x1), ff_y_to_bmp_y(y1), ff_x_to_bmp_x(x2) , ff_y_to_bmp_y(y2))
    y_diff = y2-y1
    for col in range(y_diff):
        current_y = y1 + (y_diff - col)
        bmp_y = ff_y_to_bmp_y( + (current_y))
        row_data = ""
        for row in range(x2-x1):
            bmp_x = x1 + row + 10
            
            data_rgb=bmp_image.getpixel((bmp_x, bmp_y))
            #print("data rgb:", data_rgb)
            data=0
            if data_rgb==(255,255,255):
                data = 1
            #print("data:", data, bmp_x, bmp_y)
            row_data += ' %d' % (data,)

        print("%3d(%3d) %s" % (bmp_y,current_y,row_data))
            

#bmp_path = 'uni6E90.bmp'
#bmp_path = '/Users/chunyuyao/Documents/noto/U_13898.png'
bmp_path = '/Users/chunyuyao/Documents/noto/bmp/U_39636.png'
bmp_image = Image.open( bmp_path )

print("bmp_image.height:", bmp_image.height)
print("bmp_image.width:", bmp_image.width)

#for i_vertical in range(bmp_image.height):
#i_vertical=339
#line_horizon = [bmp_image.getpixel((i_horizon, i_vertical)) for i_horizon in range(bmp_image.width) ]
#print(*line_horizon)
#print("x:",x)
'''
for y in range(160, 170):
    row=""
    for x in range(410,410+10):
        data=bmp_image.getpixel((x, y))
        if data > 0:
            data=1
        #print()
        row+=' %d'%(data,)

    print("%3d %s" % (y,row))
'''

x1=469
y1=750

x2=479
y2=822
print("FF coordinate x,y to x,y",x1,y1,x2,y2)
ff_block_sum(bmp_image, x1,y1,x2,y2)

bmp_image.close()