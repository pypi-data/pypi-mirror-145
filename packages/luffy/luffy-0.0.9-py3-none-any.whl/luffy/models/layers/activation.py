import torch
import torch.nn.functional as F
from torch import nn

__all__ = ['Swish', 'SwiGLU']


class Swish(nn.Module):
    def __init__(self, use_hard=False):
        super(Swish, self).__init__()
        self.use_hard = use_hard

    def forward(self, x):
        if self.use_hard:
            return x * F.relu6(x + 3, inplace=True) / 6
        return x * torch.sigmoid(x)


class SwiGLU(nn.Module):
    def forward(self, x):
        x, gate = x.chunk(2, dim=-1)
        return F.silu(gate) * x
