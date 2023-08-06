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
import torch
import torch.nn as nn

from PyDeepfake.models.base import BaseNetwork
from PyDeepfake.utils.registries import MODEL_REGISTRY

'''
MODEL:
  MODEL_NAME: ResNet50
  PRETRAINED: True
'''
REPO_OR_DIR = 'pytorch/vision:v0.10.0'


class BaseResNet(BaseNetwork):
    def __init__(self, model_cfg) -> None:
        super().__init__()
        self.net = nn.Sequential(
            torch.hub.load(
                REPO_OR_DIR, self.net_name, pretrained=model_cfg['PRETRAINED']
            ),
            nn.Linear(1000, 2),
        )

    def forward(self, samples):
        x = samples['img']
        return {'logits': self.net(x)}


@MODEL_REGISTRY.register()
class ResNet18(BaseResNet):
    def __init__(self, model_cfg) -> None:
        self.net_name = 'resnet18'
        super().__init__(model_cfg)


@MODEL_REGISTRY.register()
class ResNet34(BaseResNet):
    def __init__(self, model_cfg) -> None:
        self.net_name = 'resnet34'
        super().__init__(model_cfg)


@MODEL_REGISTRY.register()
class ResNet50(BaseResNet):
    def __init__(self, model_cfg) -> None:
        self.net_name = 'resnet50'
        super().__init__(model_cfg)


@MODEL_REGISTRY.register()
class ResNet101(BaseResNet):
    def __init__(self, model_cfg) -> None:
        self.net_name = 'resnet101'
        super().__init__(model_cfg)


@MODEL_REGISTRY.register()
class ResNet152(BaseResNet):
    def __init__(self, model_cfg) -> None:
        self.net_name = 'resnet152'
        super().__init__(model_cfg)


# if __name__ == '__main__':
#     cfg={}
#     cfg['INPUT_FEATURE']=30*30*3
#     cfg['HIDDEN_SIZE']=128
#     cfg['OUTPUT_FEATURE']=2
#     input=torch.rand(16,3,380,380)
#     samples={}
#     samples['img']=input
#     net = ResNet50(cfg)
#     output=net(samples)
#     print(output.shape)
#     print(output)
