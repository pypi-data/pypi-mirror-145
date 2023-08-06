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
from kornia import xla_is_available
import torch
import torch.nn as nn
import torch.nn.functional as F

from .base import BaseNetwork
from PyDeepfake.utils.registries import MODEL_REGISTRY


@MODEL_REGISTRY.register()
class MesoInception4(BaseNetwork):
    def __init__(self, model_cfg):
        super(MesoInception4, self).__init__()
        num_classes = model_cfg["num_classes"] if model_cfg["num_classes"] != 2 else 1
        self.inception_conv1 = InceptionLayer(3, 1, 4, 4, 2)
        self.inception_conv2 = InceptionLayer(11, 2, 4, 4, 2)
        self.conv3 = Meso1(12, 16, 5, 2)
        self.conv4 = Meso1(16, 16, 5, 4)
        self.fc1 = nn.Sequential(
            nn.Dropout2d(0.5), nn.Linear(16 * 8 * 8, 16), nn.LeakyReLU(0.1)
        )
        self.fc2 = nn.Sequential(nn.Dropout2d(0.5), nn.Linear(16, num_classes))

    def forward(self, x):
        x = self.inception_conv1(x)
        x = self.inception_conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = F.sigmoid(x)
        output = {"logits": x}
        return output


class InceptionLayer(BaseNetwork):
    def __init__(
        self, in_channels, out_channel1, out_channel2, out_channel3, out_channel4
    ):
        super(InceptionLayer, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, out_channel1, padding="same", kernel_size=1),
            nn.ReLU(),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels, out_channel2, 1, padding="same"),
            nn.ReLU(),
            nn.Conv2d(out_channel2, out_channel2, 3, padding="same"),
            nn.ReLU(),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels, out_channel3, 1, padding="same"),
            nn.ReLU(),
            nn.Conv2d(out_channel3, out_channel3, 3, padding="same", dilation=2),
            nn.ReLU(),
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels, out_channel4, 1, padding="same"),
            nn.ReLU(),
            nn.Conv2d(out_channel4, out_channel4, 3, padding="same", dilation=3),
            nn.ReLU(),
        )
        self.bn = nn.BatchNorm2d(
            out_channel1 + out_channel2 + out_channel3 + out_channel4
        )
        self.pool = nn.MaxPool2d((2, 2))

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        x4 = self.conv4(x)
        y = torch.cat((x1, x2, x3, x4), dim=1)
        y = self.bn(y)
        y = self.pool(y)
        return y


class Meso1(BaseNetwork):
    def __init__(self, in_channels, out_channels, kernel_size, pool_size):
        super(Meso1, self).__init__()
        self.conv = nn.Conv2d(
            in_channels, out_channels, kernel_size, padding="same", bias=True
        )
        self.relu = nn.ReLU(inplace=True)
        self.bn = nn.BatchNorm2d(out_channels)
        self.pool = nn.MaxPool2d((pool_size, pool_size))

    def forward(self, x):
        x = self.conv(x)
        x = self.relu(x)
        x = self.bn(x)
        x = self.pool(x)
        return x


if __name__ == "__main__":
    from torchsummary import summary

    cfg = {"num_classes": 2, "type": "MesoInception4"}
    model = MesoInception4(cfg)
    model.cuda()
    summary(model, input_size=(3, 256, 256), batch_size=64, device="cuda")
