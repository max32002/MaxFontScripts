#!/usr/bin/env python3
#encoding=utf-8

import os
import cv2
import numpy as np

def ff_x_to_bmp_x(x):
    offset = 0
    return x + offset

def ff_y_to_bmp_y(y, y_offset):
    top = 900 - y_offset
    return top + (y * -1)

def ff_image_block(bmp_image, x1,y1,x2,y2,x3,y3,x4,y4,y_offset):
    bmp_x1 = ff_x_to_bmp_x(x1)
    bmp_y1 = ff_y_to_bmp_y(y1,y_offset)
    bmp_x2 = ff_x_to_bmp_x(x2)
    bmp_y2 = ff_y_to_bmp_y(y2,y_offset)
    bmp_x3 = ff_x_to_bmp_x(x3)
    bmp_y3 = ff_y_to_bmp_y(y3,y_offset)
    bmp_x4 = ff_x_to_bmp_x(x4)
    bmp_y4 = ff_y_to_bmp_y(y4,y_offset)
    print("bmp coordinate x,y to x,y",bmp_x1,bmp_y1,bmp_x2,bmp_y2,bmp_x3,bmp_y3,bmp_x4,bmp_y4)

    # create mask with zeros
    mask = np.zeros((bmp_image.shape), dtype=np.uint8)
    mask_value = (128,128,128)
    #mask_value = (128)

    pts = np.array( [[[bmp_x1,bmp_y1],[bmp_x2,bmp_y2],[bmp_x3,bmp_y3],[bmp_x4,bmp_y4]]], dtype=np.int32 )
    cv2.fillPoly(mask, pts, mask_value )

    # get color values
    values = bmp_image[np.where((mask == mask_value).all(axis=2))]
    #values = bmp_image[np.where((mask == mask_value).all())]
    #print(values)

    diff_x = x2-x1
    diff_y = y2-y3
    print("diff_x:", diff_x)
    print("diff_y:", diff_y)


    flag_avg = 0.0
    flag_total = 0

    row = ""
    idx=0
    values_formated = []
    for item in values:
        idx += 1
        flag = 1
        if item[0]==0:
            flag = 0
        row += " %d" % (flag)
        flag_total += flag
        values_formated.append(flag)
        if idx % (diff_x+1) == 0:
            print((diff_x+1), row)
            row = ""
            #print(idx, flag)

    if idx > 0:
        flag_avg = flag_total / idx

    print("count:", idx)
    print("total:", flag_total)
    print("average:", flag_avg)

    #np_re = np.array(values_formated)
    #np2 = np_re.reshape([diff_x+1,diff_y+1])
    #print("np2:", np2)


    '''
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
            
    '''

#bmp_path = 'uni6E90.bmp'
#bmp_path = '/Users/chunyuyao/Documents/noto/U_13898.png'

# 體
#bmp_path = '/Users/chunyuyao/Documents/noto/bmp/svg/U_39636.bmp'

# 㙊
ch='綎'
bmp_path = '/Users/chunyuyao/Documents/noto/bmp/U_%d.bmp' % (ord(ch))

bmp_image = None

if os.path.exists(bmp_path):
    print("bmp_path:", bmp_path)
    #bmp_image = cv2.imread( bmp_path, cv2.IMREAD_GRAYSCALE)
    bmp_image = cv2.imread( bmp_path, cv2.IMREAD_COLOR)
    #cv2.IMREAD_COLOR     為預設值
    #cv2.IMREAD_GRAYSCALE 以灰階的格式來讀取圖片。 
    #cv2.IMREAD_UNCHANGED 讀取圖片中所有的 channels，包含透明度的 channel。

    print("image.shape:", bmp_image.shape)
else:
    print("exported image not exist:", bmp_path)
    pass

data_top=0
if not bmp_image is None:
    threshold=0
    data_top=0
    h, w, d = bmp_image.shape

    is_match_data = False
    for y in range(h):
        if y==0:
            continue
        if y==h-1:
            continue

        for x in range(w):
            if bmp_image[y, x][0] == threshold and bmp_image[y+1, x][0] == threshold and bmp_image[y-1, x][0] == threshold:
               print("bingo:", x, y-1, bmp_image[x, y])
               is_match_data = True
               data_top=y-1
               break
        if is_match_data:
            break

    print("data_top:", data_top)

'''


data_top=0
data_index = 0

values = bmp_image[np.where((mask == mask_value).all(axis=2))]
for item in im:
    data_index +=1
    if item[0]==0:
        break
data_top = int(data_index / 1000)
print("data_top:", data_top)

#for i_vertical in range(bmp_image.height):
#i_vertical=339
#line_horizon = [bmp_image.getpixel((i_horizon, i_vertical)) for i_horizon in range(bmp_image.width) ]
#print(*line_horizon)
#print("x:",x)
'''

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

# for debug 體
x1=469
y1=761

x2=474
y2=761

x3=474
y3=757

x4=469
y4=757

# for debug 綎
x1=565
y1=764

x2=473
y2=482

x3=532
y3=482

x4=543
y4=483



FF_TOP=838
BMP_TOP=data_top
y_offset = (900 - FF_TOP) - BMP_TOP

print("FF coordinate x,y to x,y",x1,y1,x2,y2,x3,y3,x4,y4)
ff_image_block(bmp_image,x1,y1,x2,y2,x3,y3,x4,y4, y_offset)


#cv2.imshow('image', bmp_image)
#cv2.waitKey()

