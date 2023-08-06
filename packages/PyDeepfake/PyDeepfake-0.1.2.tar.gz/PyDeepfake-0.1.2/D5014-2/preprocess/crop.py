import cv2
import numpy as np
import argparse
import os
import random
from time import time
from multiprocessing import Process
import pickle
from retinaface.pre_trained_models import get_model
import torch

random.seed(0)

parser = argparse.ArgumentParser()
parser.add_argument('--root_dir', type=str,
                    default='/share/test/ouyang/celeb-df-v1')
# parser.add_argument('--save_root_dir', type=str,
#                     default='/home/alan/code/tmp/ForgeryNet/Validation')
parser.add_argument('--process', type=int, default=8)
# parser.add_argument('--save_path', type=str,
#                     default='./image_list_val_retina.txt')
args = parser.parse_args()
root_dir = args.root_dir
# save_root_dir = args.save_root_dir
num_process = args.process
# raw_images_path = os.path.join(root_dir, 'raw_image')
# extract_images_path = os.path.join(save_root_dir, 'image')
image_list_path = os.path.join(root_dir, 'raw_image_list.txt')
new_image_list_path = os.path.join(root_dir, 'image_list.txt')
if not os.path.exists('pkl'):
    os.mkdir('pkl')
os.system('rm -rf ./tmp/* ./tmp2/*')


def can_seg(img_path, save_path, model=None, scale=1.3):
    img = cv2.imread(img_path)
    h, w, c = img.shape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    annotation = model.predict_jsons(
        img, confidence_threshold=0.7)  # , nms_threshold=.3)
    if len(annotation[0]['bbox']) == 0:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite('./tmp2/%d.jpg' % (random.randint(1, 100)), img)
        return False
    x1, y1, x2, y2 = annotation[0]['bbox']
    # print(x1, y1, x2, y2)
    x1, y1, x2, y2 = list(map(int, [x1-(x2-x1)*(scale-1)/2, y1-(y2-y1)*(
        scale-1)/2,  x2+(x2-x1)*(scale-1)/2, y2+(y2-y1)*(scale-1)/2]))
    # print(x1, y1, x2, y2, '\n')
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w-1, x2), min(h-1, y2)
    img_face = img[y1:y2, x1:x2, :]
    # print(img_face)
    img_face = cv2.cvtColor(img_face, cv2.COLOR_RGB2BGR)
    # save_path = './tmp/%d.jpg' % random.randint(1, 1000)
    cv2.imwrite(save_path, img_face)
    return True


def solve(process_id, sub_image_list, sub_new_image_list=[]):
    device = 'cuda:%d' % process_id
    model = get_model("resnet50_2020-07-20", max_size=1024,
                      device=device)
    model.eval()
    tot_image = len(sub_image_list)
    cnt = 0
    st = time()
    for item in sub_image_list:
        rel_path = item[0]
        cnt += 1
        raw_image_path = os.path.join(root_dir, rel_path)
        save_image_path = os.path.join(root_dir,'img', os.path.basename(rel_path))
        # print(raw_image_path, save_image_path)
        # test
        if cnt % 5 == 0:
            rt = time()-st
            progress = cnt/tot_image
            remain = rt/progress*(1-progress)
            print(cnt, '/', tot_image, 'run time: %.2fmin' % (rt/60), 'remain: % .2fhours' %
                  (remain/60/60), process_id)
            print("can seg: %d / %d rate: %.2f%%" %
                  (len(sub_new_image_list), cnt, len(sub_new_image_list)*100 / cnt))
        ###
        if can_seg(raw_image_path, save_image_path, model):
            sub_new_image_list.append(item)
    print("process ", process_id, ' done')
    print("total image:", tot_image)
    print('can seg image:', len(sub_new_image_list))
    with open('./pkl/%d.pkl' % process_id, 'wb')as w:
        pickle.dump(sub_new_image_list, w)


if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn')
    new_dir=  os.path.join(root_dir,'img')
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    if not os.path.exists('pkl'):
        os.mkdir('pkl')

    image_list = []
    new_image_list = []
    with open(image_list_path, 'r')as f:
        for line in f:
            d = line.strip().split()
            l1, l2= d
            image_list.append([l1, l2])

    # multi-process, split image list
    sub_image_list = []
    n = len(image_list)
    print(n)
    step = n//num_process
    j = 0
    for i in range(0, n, step):
        j += 1
        if j == num_process:
            sub_image_list.append(image_list[i:n])
            break
        else:
            sub_image_list.append(image_list[i:i+step])

    process_list = []
    for i, item in enumerate(sub_image_list):
        cur_process = Process(target=solve, args=(
            i, item))
        process_list.append(cur_process)

    for process in process_list:
        process.start()
    for process in process_list:
        process.join()

    # merge sub image list
    new_image_list = []
    for i in range(num_process):
        with open('./pkl/%d.pkl' % (i), 'rb')as f:
            sub = pickle.load(f)
        new_image_list.extend(sub)

    random.shuffle(new_image_list)
    with open(new_image_list_path, 'w')as w:
        for a, b in new_image_list:
            print('%s %s' % (a, b), file=w)