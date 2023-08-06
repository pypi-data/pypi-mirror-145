import cv2
import os

root = r'/share/test/ouyang/celeb-df-v1'

image_list=[]
for rt,dirs,files in os.walk(root):
    if '-img' in rt:
        for file in files:
            path = os.path.join(rt, file)
            path = os.path.relpath(path, root)
            label = 0 if 'real' in rt else 1
            image_list.append([path,label])
image_list_path = os.path.join(root,'raw_image_list.txt')
with open(image_list_path,'w') as w:
    for e in image_list:
        print(e[0],e[1],file=w)