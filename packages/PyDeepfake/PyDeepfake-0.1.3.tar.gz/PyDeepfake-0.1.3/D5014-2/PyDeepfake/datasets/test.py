'''
Copyright 2022 fvl

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import os
from PyDeepfake.datasets.FFDF import FFDF
from PyDeepfake.datasets.ForgeryNet import ForgeryNet

if __name__ == '__main__':
    # usage-test
    from torch.utils.data import DataLoader

    """
    img_size = cfg['IMG_SIZE']
    scale_rate = cfg['SCALE_RATE']
    rotate_angle = cfg['ROTATE_ANGLE']
    cutout_h = cfg['CUTOUT_H']
    cutout_w = cfg['CUTOUT_W']
    compression_low = cfg['COMPRESSION_LOW']
    compression_high = cfg['COMPRESSION_HIGH']
    """

    ffdf_data_cfg = {
        'IMG_SIZE': 320,
        'SCALE_RATE': 8 / 7,
        'ROTATE_ANGLE': 30,
        'CUTOUT_H': 32,
        'CUTOUT_W': 32,
        'COMPRESSION_LOW': 65,
        'COMPRESSION_HIGH': 80,
        'ROOT_DIR': '/share/test/ouyang/FF++_face',
        'DATASET_NAME': 'FFDF',
        'TRAIN_INFO_TXT': '/share/home/zhangchao/works/FFDF_splits_train_low.txt',
        'VAL_INFO_TXT': '/share/home/zhangchao/works/FFDF_splits_val_low.txt',
        'TEST_INFO_TXT': '/share/home/zhangchao/works/FFDF_splits_test_low.txt',
    }
    forgerynet_data_cfg = {
        'IMG_SIZE': 320,
        'SCALE_RATE': 8 / 7,
        'ROTATE_ANGLE': 30,
        'CUTOUT_H': 32,
        'CUTOUT_W': 32,
        'COMPRESSION_LOW': 65,
        'COMPRESSION_HIGH': 80,
        'ROOT_DIR': '/share/test/ouyang/ForgeryNet',
        'DATASET_NAME': 'ForgeryNet',
        'TRAIN_INFO_TXT': '',
        'VAL_INFO_TXT': '',
        'TEST_INFO_TXT': '',
    }
    testDataset = ForgeryNet(forgerynet_data_cfg, mode='val')
    Dataloader_test = DataLoader(
        testDataset, batch_size=1, shuffle=True, num_workers=1
    )

    for i_batch, sample_batched in enumerate(Dataloader_test):
        print('img:', sample_batched['img'].size())
        print('mask:', sample_batched['mask'].size())
