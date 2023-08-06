import math

import torch.nn as nn

from .layers import Swish

# Paper suggests 0.99 momentum, for TensorFlow. Equivalent PyTorch momentum is (1.0 - tensorflow).
_BN_MOMENTUM = 1 - 0.99

__all__ = ['EfficientNetB0', 'EfficientNetB1', 'EfficientNetB2', 'EfficientNetB3', 'EfficientNetB4', 'EfficientNetB5',
           'EfficientNetB6', 'EfficientNetB7', 'EfficientNetB8', 'EfficientNetL2']


class SEBlock(nn.Module):
    def __init__(self, in_ch, mid_ch, act_module=Swish()):
        super(SEBlock, self).__init__()
        self.layer = nn.Sequential(
            # 1. sq
            nn.AdaptiveAvgPool2d((1, 1)),
            # 2. ex
            # nn.Linear(in_ch, mid_ch),
            nn.Conv2d(in_ch, mid_ch, 1, 1),
            act_module,
            # nn.Linear(mid_ch, in_ch),
            nn.Conv2d(mid_ch, in_ch, 1, 1),
            nn.Sigmoid())

    def forward(self, input):
        return self.layer(input) * input


class MBConv(nn.Module):
    """A class of MBConv: Mobile Inverted Residual Bottleneck."""

    def __init__(self, in_ch, out_ch, kernel_size, stride, expansion_factor, act_module=Swish(), use_se=True,
                 se_ratio=0.25, bn_momentum=_BN_MOMENTUM):
        super(MBConv, self).__init__()
        mid_ch = in_ch * expansion_factor
        self.apply_residual = (in_ch == out_ch and stride == 1)
        self.layer = nn.Sequential(
            # 1. Conv1x1, BN, Relu (Pointwise)
            nn.Conv2d(in_ch, mid_ch, 1, stride=1, bias=False),
            nn.BatchNorm2d(mid_ch, momentum=bn_momentum),
            act_module,
            # 2. DWConv, BN, Relu (Depthwise)
            nn.Conv2d(mid_ch, mid_ch, kernel_size, padding=kernel_size // 2, stride=stride, groups=mid_ch, bias=False),
            nn.BatchNorm2d(mid_ch, momentum=bn_momentum),
            act_module,
            # 3. SE (Pooling, FC, Relu, FC, Sigmoid, MUL)
            SEBlock(mid_ch, max(1, int(se_ratio * mid_ch)), act_module) if use_se else nn.Identity(),
            # 4. Conv1x1, BN (Linear pointwise. Note that there's no activation.)
            nn.Conv2d(mid_ch, out_ch, 1, stride=1, bias=False),
            nn.BatchNorm2d(out_ch, momentum=bn_momentum))

    def forward(self, input):
        if self.apply_residual:
            return self.layer(input) + input
        else:
            return self.layer(input)


def _stack(in_ch, out_ch, kernel_size, stride, exp_factor, repeat, act_module=Swish(), use_se=True, se_ratio=0.25,
           bn_momentum=_BN_MOMENTUM):
    """ Creates a stack of inverted residuals. """
    assert repeat >= 1
    # First one has no skip, because feature map size changes.
    first = MBConv(in_ch, out_ch, kernel_size, stride, exp_factor, act_module=act_module, use_se=use_se,
                   se_ratio=se_ratio, bn_momentum=bn_momentum)
    remaining = []
    for _ in range(1, repeat):
        remaining.append(MBConv(out_ch, out_ch, kernel_size, 1, exp_factor, act_module=act_module, use_se=use_se,
                                se_ratio=se_ratio, bn_momentum=bn_momentum))
    return nn.Sequential(first, *remaining)


def _round_to_multiple_of(val, divisor, round_up_bias=0.9):
    """ Asymmetric rounding to make `val` divisible by `divisor`. With default
    bias, will round up, unless the number is no more than 10% greater than the
    smaller divisible value, i.e. (83, 8) -> 80, but (84, 8) -> 88. """
    assert 0.0 < round_up_bias < 1.0
    new_val = max(divisor, int(val + divisor / 2) // divisor * divisor)
    return new_val if new_val >= round_up_bias * val else new_val + divisor


def _get_depths(alpha):
    """ Scales tensor depths as in reference MobileNet code, prefers rouding up rather than down. """
    depths = [32, 16, 24, 40, 80, 112, 192, 320, 1280]
    return [_round_to_multiple_of(depth * alpha, 8) for depth in depths]


def _get_repeats(beta):
    repeats = [1, 1, 2, 2, 3, 3, 4, 1, 1]
    return [math.ceil(repeat * beta) for repeat in repeats]


class EfficientNet(nn.Module):
    """EfficientNet.

        A PyTorch implement of : `EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
        <https://arxiv.org/abs/1905.11946>`_"""

    # B0(input_size 224*224 width->alpha=1.2, depth->beta=1.1, resolution->gamma=1.15)
    def __init__(self, alpha=1.2, beta=1.1, num_classes=1000, dropout=0.2, use_se=True, se_ratio=0.25, act_module=None,
                 bn_momentum=_BN_MOMENTUM):
        super(EfficientNet, self).__init__()
        depths = _get_depths(alpha)
        repeats = _get_repeats(beta)
        # default is Swish(), for example if you want to use relu, pass nn.Relu(inplace=True) param.
        act_module = act_module or Swish()
        # stage 1: Conv3x3
        self.stage1 = nn.Sequential(
            nn.Conv2d(3, depths[0], 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(depths[0], momentum=bn_momentum),
            act_module)

        # stage 2: MBConv1, k3x3
        self.stage2 = _stack(depths[0], depths[1], 3, 1, 1, repeats[1], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 3: MBConv6, k3x3
        self.stage3 = _stack(depths[1], depths[2], 3, 2, 6, repeats[2], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 4: MBConv6, k5x5
        self.stage4 = _stack(depths[2], depths[3], 5, 2, 6, repeats[3], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 5: MBConv6, k3x3
        self.stage5 = _stack(depths[3], depths[4], 3, 2, 6, repeats[4], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 6: MBConv6, k5x5
        self.stage6 = _stack(depths[4], depths[5], 5, 1, 6, repeats[5], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 7: MBConv6, k5x5
        self.stage7 = _stack(depths[5], depths[6], 5, 2, 6, repeats[6], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 8: MBConv6, k3x3
        self.stage8 = _stack(depths[6], depths[7], 3, 1, 6, repeats[7], act_module=act_module, use_se=use_se,
                             se_ratio=se_ratio, bn_momentum=bn_momentum)
        # stage 9: Conv1x1 & Pooling & FC
        self.stage9 = nn.Sequential(
            nn.Conv2d(depths[7], depths[8], 1, bias=False),
            nn.BatchNorm2d(depths[8], momentum=bn_momentum),
            act_module)

        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout, inplace=True),
            nn.Linear(depths[8], num_classes))

        self._initialize_weights()

    def forward(self, x):
        # in paper EfficientNet, classification task return x.
        # in paper EfficientDet, detection/segmentation task fpn struct return (c1, c2, c3, c4, c5),
        x = self.stage1(x)  # (b, 3, h, w) -> (b, 32*, h/2, w/2)
        c1 = self.stage2(x)  # (b, 32*, h/2, w/2) -> (b, 16*, h/2, w/2)
        c2 = self.stage3(c1)  # (b, 16*, h/2, w/2) -> (b, 24*, h/4, w/4)
        c3 = self.stage4(c2)  # (b, 24*, h/4, w/4) -> (b, 40*, h/8, w/8)
        x = self.stage5(c3)  # (b, 40*, h/8, w/8) -> (b, 80*, h/16, w/16)
        c4 = self.stage6(x)  # (b, 80*, h/16, w/16) -> (b, 112*, h/16, w/16)
        x = self.stage7(c4)  # (b, 112*, h/16, w/16) -> (b, 192*, h/32, w/32)
        c5 = self.stage8(x)  # (b, 192*, h/32, w/32) -> (b, 320*, h/32, w/32)
        x = self.stage9(c5)  # (b, 320*, h/32, w/32) -> (b, 1280*, h/32, w/32)
        # Equivalent to global avgpool and removing H and W dimensions.
        x = x.mean([2, 3])  # (b, 1280*, h/32, w/32) -> (b, 3280*)
        x = self.classifier(x)  # (b, 3280*) -> (b, c)
        # print(c1.size(), c2.size(), c3.size(), c4.size(), c5.size())
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out")
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Linear):
                nn.init.kaiming_uniform_(m.weight, mode="fan_out", nonlinearity="sigmoid")
                nn.init.zeros_(m.bias)


def efficientnet_params(model_name):
    """Get efficientnet params based on model name, from official code, differ with paper"""
    params_dict = {
        # (width_coefficient, depth_coefficient, resolution, dropout_rate)
        'efficientnet-b0': (1.0, 1.0, 224, 0.2),
        'efficientnet-b1': (1.0, 1.1, 240, 0.2),
        'efficientnet-b2': (1.1, 1.2, 260, 0.3),
        'efficientnet-b3': (1.2, 1.4, 300, 0.3),
        'efficientnet-b4': (1.4, 1.8, 380, 0.4),
        'efficientnet-b5': (1.6, 2.2, 456, 0.4),
        'efficientnet-b6': (1.8, 2.6, 528, 0.5),
        'efficientnet-b7': (2.0, 3.1, 600, 0.5),
        'efficientnet-b8': (2.2, 3.6, 672, 0.5),
        'efficientnet-l2': (4.3, 5.3, 800, 0.5),
    }
    return params_dict[model_name]


class EfficientNetB0(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b0')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB1(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b1')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB2(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b2')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB3(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b3')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB4(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b4')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB5(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b5')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB6(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b6')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB7(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b7')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetB8(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-b8')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)


class EfficientNetL2(EfficientNet):
    def __init__(self, **kwargs):
        alpha, beta, _, dropout_rate = efficientnet_params('efficientnet-l2')
        super().__init__(alpha=alpha, beta=beta, dropout=dropout_rate, **kwargs)
