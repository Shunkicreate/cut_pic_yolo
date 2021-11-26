import cv2
import numpy as np
    

#画像の読み込み
img=cv2.imread('cat/newyork.jpg',cv2.IMREAD_COLOR)
h,w=img.shape[:2]
separate_x=4
separate_y=3
#画像の分割処理
cx=0
cy=0
for i in range(separate_x):
    for j in range(separate_y):
        separate_pic=img[cy:cy+int(h/separate_y),cx:cx+int(w/separate_x),:]
        cv2.imwrite('cat/separate/newyork_x'+str(i)+'_y'+str(j)+'.jpg',separate_pic)
        cy=cy+int(h/separate_y)
    cy=0
    cx=cx+int(w/separate_x)