# Copyright (c) 2020 Sony Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict

import nnabla.functions as F

from ..... import module as Mo
from ..ofa_utils.common_tools import make_divisible


class SEModule(Mo.Module):

    r"""Squeeze-and-Excitation module, that adaptively recalibrates channel-wise
        feature responces by explicitlly modelling interdependencies
        between channels.

    Args:
        channel (int): The number of input channels.
        reduction (int, optional): The reduction rate used to determine
            the number of middle channels.

    References:
    [1] Hu, Jie, Li Shen, and Gang Sun. "Squeeze-and-excitation networks."
        Proceedings of the IEEE conference on computer vision and pattern
        recognition. 2018.
    """

    REDUCTION = 4

    def __init__(self, channel, reduction=None, name=''):
        self._name = name
        self._scope_name = f'<semodule at {hex(id(self))}>'

        self._channel = channel
        self.reduction = SEModule.REDUCTION if reduction is None else reduction

        num_mid = make_divisible(self._channel // self.reduction)

        self.fc = Mo.Sequential(OrderedDict([
            ('reduce', Mo.Conv(
                self._channel, num_mid, (1, 1), pad=(0, 0), stride=(1, 1), with_bias=True)),
            ('relu', Mo.ReLU()),
            ('expand', Mo.Conv(
                num_mid, self._channel, (1, 1), pad=(0, 0), stride=(1, 1), with_bias=True)),
            ('h_sigmoid', Mo.Hsigmoid())
        ]))

    def call(self, input):
        y = F.mean(input, axis=(2, 3), keepdims=True)
        y = self.fc(y)
        return input * y
