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

'''
OPTIMIZER:
  OPTIMIZER_METHOD: sgd
  BASE_LR: 0.0001
  MOMENTUM: 0
  DAMPENING: 0
  WEIGHT_DECAY: 0
  NESTEROV: False

OPTIMIZER:
  OPTIMIZER_METHOD: adam
  BASE_LR: 0.001
  ADAM_BETAS: [0.9, 0.999]
  EPS: 0.00000001
  WEIGHT_DECAY: 0
  AMSGRAD: False

OPTIMIZER:
  OPTIMIZER_METHOD: adamw
  BASE_LR: 0.001
  ADAM_BETAS: [0.9, 0.999]
  EPS: 0.00000001
  WEIGHT_DECAY: 0.01
  AMSGRAD: False
'''


def build_optimizer(optim_params, cfg):
    """
    Construct a stochastic gradient descent or ADAM optimizer with momentum.
    Details can be found in:
    Herbert Robbins, and Sutton Monro. "A stochastic approximation method."
    and
    Diederik P.Kingma, and Jimmy Ba.
    "Adam: A Method for Stochastic Optimization."
    Args:
        model (model): model to perform stochastic gradient descent
        optimization or ADAM optimization.
        cfg (dict): configs of hyper-parameters of SGD or ADAM, includes base
        learning rate,  momentum, weight_decay, dampening, and etc.
    """
    optimizer_cfg = cfg['OPTIMIZER']
    print('optimizer: ')
    print(optimizer_cfg)
    if optimizer_cfg['OPTIMIZER_METHOD'] == "sgd":
        return torch.optim.SGD(
            optim_params,
            lr=optimizer_cfg['BASE_LR'],
            momentum=optimizer_cfg['MOMENTUM'],
            # dampening=optimizer_cfg['DAMPENING'],
            # weight_decay=optimizer_cfg['WEIGHT_DECAY'],
            # nesterov=optimizer_cfg['NESTEROV'],
        )
    elif optimizer_cfg['OPTIMIZER_METHOD'] == "rmsprop":
        return torch.optim.RMSprop(
            optim_params,
            lr=optimizer_cfg['BASE_LR'],
            alpha=optimizer_cfg['ALPHA'],
            eps=optimizer_cfg['EPS'],
            weight_decay=optimizer_cfg['WEIGHT_DECAY'],
            momentum=optimizer_cfg['MOMENTUM'],
        )
    elif optimizer_cfg['OPTIMIZER_METHOD'] == "adam":
        return torch.optim.Adam(
            optim_params,
            lr=optimizer_cfg['BASE_LR'],
            betas=optimizer_cfg['ADAM_BETAS'],
            eps=optimizer_cfg['EPS'],
            weight_decay=optimizer_cfg['WEIGHT_DECAY'],
            amsgrad=optimizer_cfg['AMSGRAD'],
        )
    elif optimizer_cfg['OPTIMIZER_METHOD'] == "adamw":
        return torch.optim.AdamW(
            optim_params,
            lr=optimizer_cfg['BASE_LR'],
            betas=optimizer_cfg['ADAM_BETAS'],
            eps=optimizer_cfg['EPS'],
            weight_decay=optimizer_cfg['WEIGHT_DECAY'],
            amsgrad=optimizer_cfg['AMSGRAD'],
        )
    else:
        raise NotImplementedError(
            "Does not support {} optimizer".format(
                optimizer_cfg['OPTIMIZER_METHOD']
            )
        )
