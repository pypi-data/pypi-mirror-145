import cv2
import os
suf='-raw-img'
def video2img(video_path, sample=16):
    cap = cv2.VideoCapture(video_path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if num_frames == 0:
        print("err frame=0", video_path)
        return False, -2, []
    stride = num_frames//sample+1
    order = [j for i in range(stride) for j in range(i, num_frames, stride)]
    frame_dict = {}
    mark = []
    i, c = 0, 0
    while True:
        i += 1
        j = order[i % len(order)]
        cap.set(cv2.CAP_PROP_POS_FRAMES, j)
        flag, frame = cap.read()

        c+=1
        name = os.path.basename(video_path).replace('.mp4','')+'_%02d'%c+'.jpg'
        img_path = os.path.join(os.path.dirname(video_path)+suf, name)
        cv2.imwrite(img_path, frame)
        if c == sample:
            break

    cap.release()

root = r'/share/test/ouyang/celeb-df-v1'


for rt,dirs,files in os.walk(root):
    for dir in dirs:
        if suf in dir:
            continue
        path = os.path.join(rt, dir)
        new_path = path+suf
        print(new_path)
        try:
            os.mkdir(new_path)
        except Exception as e:
            print(e)

for rt,dirs,files in os.walk(root):
    print(rt, dirs)
    if len(files)<2:
        continue
    for file in files:
        if '.mp4' in file:
            path = os.path.join(rt,file)
            # print(path)
            video2img(path)
