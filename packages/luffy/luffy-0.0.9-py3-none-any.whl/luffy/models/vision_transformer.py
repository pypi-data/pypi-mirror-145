import torch
from einops import repeat
from einops.layers.torch import Rearrange
from torch import nn
from torch.nn.modules.utils import _pair

from .layers import TransformerBlock

__all__ = ['ViTB16', 'ViTB32', 'ViTL16', 'ViTL32']


class VisionTransformer(nn.Module):
    """Vision Transformer.

        A PyTorch implement of : `An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
        <https://arxiv.org/abs/2010.11929>`_"""

    def __init__(self, *, image_size, channels=3, patch_size, dim, depth, num_heads, mlp_dim, drop=0., attn_drop=0.,
                 num_classes, pool='cls'):
        super().__init__()
        image_height, image_width = _pair(image_size)
        patch_height, patch_width = _pair(patch_size)

        assert image_height % patch_height == 0 and image_width % patch_width == 0, \
            'Image size must be divisible by patch size!'

        seq_length = (image_height // patch_height) * (image_width // patch_width)
        patch_dim = channels * patch_height * patch_width
        assert pool in {'cls', 'mean'}, 'pool type must be either cls (cls token) or mean (mean pooling)'

        self.to_patch_embedding = nn.Sequential(
            Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_height, p2=patch_width),
            nn.Linear(patch_dim, dim))

        self.pos_embedding = nn.Parameter(torch.randn(1, seq_length + 1, dim))
        self.cls_token = nn.Parameter(torch.zeros(1, 1, dim))
        self.drop = nn.Dropout(drop)

        self.blocks = nn.ModuleList(
            [TransformerBlock(dim, num_heads, mlp_dim, drop, attn_drop) for _ in range(depth)])

        self.pool = pool

        self.mlp_head = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, num_classes))

    def forward(self, img):
        x = self.to_patch_embedding(img)
        b, n, _ = x.shape

        cls_tokens = repeat(self.cls_token, '1 n d -> b n d', b=b)
        x = torch.cat((cls_tokens, x), dim=1)
        x += self.pos_embedding[:, :(n + 1)]
        x = self.drop(x)

        for blk in self.blocks:
            x = blk(x)
        x = x.mean(dim=1) if self.pool == 'mean' else x[:, 0]

        return self.mlp_head(x)


def vit_params(model_name):
    params_dict = {
        'vit-b16': {'patch_size': 16, 'depth': 12, 'num_heads': 12, 'dim': 768, 'mlp_dim': 3072},
        'vit-b32': {'patch_size': 32, 'depth': 12, 'num_heads': 12, 'dim': 768, 'mlp_dim': 3072},
        'vit-l16': {'patch_size': 16, 'depth': 24, 'num_heads': 16, 'dim': 1024, 'mlp_dim': 4096},
        'vit-l32': {'patch_size': 32, 'depth': 24, 'num_heads': 16, 'dim': 1024, 'mlp_dim': 4096},
    }
    return params_dict[model_name]


class ViTB16(VisionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**vit_params('vit-b16'), **kwargs})


class ViTB32(VisionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**vit_params('vit-b32'), **kwargs})


class ViTL16(VisionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**vit_params('vit-l16'), **kwargs})


class ViTL32(VisionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**vit_params('vit-l32'), **kwargs})
