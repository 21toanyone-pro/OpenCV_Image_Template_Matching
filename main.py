import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter
from PIL import ImageFont 
from PIL import ImageDraw 
import os
import glob
import random
import natsort
 
save_num = 0 #이전 x 축을 저장하는 변수
bground_path = './or/'

bground_list = os.listdir(bground_path)
JPGLIST =list(filter(lambda x: x.find('.jpg') != -1 or x.find('.png') != -1, bground_list))
x = natsort.natsorted(JPGLIST)

folderSave = '대'
temp_path = './temp/'
temp_list = os.listdir(temp_path)
JPGLIST2 =list(filter(lambda x: x.find('.jpg') != -1 or x.find('.png') != -1, temp_list))
tmep_x = natsort.natsorted(JPGLIST2)

dir_path = 'crop/' + str(folderSave)
for k in range(len(JPGLIST2)):
    template = cv2.imread(temp_path+tmep_x[k], 0) # 템플릿 이미지
    w, h = template.shape[::-1]
    for i in range(len(JPGLIST)):
        #img2 = cv2.imread('./ori.jpg', cv2.IMREAD_COLOR) #그려줄 이미지
        print('page'+str(x[i])+'_loding...')
        img = Image.open(bground_path+x[i]) # 검사할 이미지(크롭용) 
        img_rgb = cv2.imread(bground_path+x[i]) # 검사할 이미지
        img= img.resize((1200,1872))
        img_rgb=cv2.resize(img_rgb, (1200, 1872))

        print(img_rgb.shape)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # template = cv2.imread(temp_path+'./temp.jpg', 0) # 템플릿 이미지
        # w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template, cv2.TM_CCOEFF_NORMED) #템플릿 매칭
        threshold = 0.7
        loc = []
        loc = np.where(res >= threshold)
        print(loc)
        for pt in zip(*loc[::-1]):
            area =(pt[0], pt[1], pt[0]+w, pt[1] + h)
            cropped_img = img.crop(area)
            if abs(save_num - pt[0]) < 10:
                continue
            else:
                ract = cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                if not os.path.isdir(dir_path):
                        os.mkdir(dir_path + '/')
                save_f = dir_path + '/'+str(x[i])

                if not os.path.isdir(save_f):
                        os.mkdir(save_f + '/')
                cropped_img.save(save_f+'/'+str(i)+'_'+str(pt) + '.jpg')
                save_num = pt[0]
                cv2.imwrite('./ract_'+str(i)+'.jpg', ract)