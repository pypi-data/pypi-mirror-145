from torch import nn

from .layers import ParallelTransformerBlock

__all__ = ['PaLMTony', 'PaLM8B', 'PaLM62B', 'PaLM540B']


class PaLM(nn.Module):
    """PaLM.
        A PyTorch implement of : `PaLM: Scaling Language Modeling with Pathways
        <https://arxiv.org/abs/2204.02311>`_"""

    def __init__(self, *, dim, num_tokens, depth, num_heads=8, mlp_ratio=4, drop=0., attn_drop=0.):
        super().__init__()
        self.embed = nn.Embedding(num_tokens, dim)
        self.blocks = nn.ModuleList(
            [ParallelTransformerBlock(dim, num_heads, dim * mlp_ratio, drop, attn_drop) for _ in range(depth)])

        self.mlp_head = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, num_tokens, bias=False))
        # they used embedding weight tied projection out to logits, not common, but works
        self.mlp_head[-1].weight = self.embed.weight

    def forward(self, x):
        x = self.embed(x)
        for blk in self.blocks:
            x = blk(x)

        return self.mlp_head(x)


def palm_params(model_name):
    params_dict = {
        'palm-tony': {'depth': 12, 'num_heads': 8, 'dim': 512},
        'palm-8b': {'depth': 32, 'num_heads': 16, 'dim': 4096},
        'palm-62b': {'depth': 64, 'num_heads': 32, 'dim': 8192},
        'palm-540b': {'depth': 118, 'num_heads': 48, 'dim': 18432},
    }
    return params_dict[model_name]


class PaLMTony(PaLM):
    def __init__(self, **kwargs):
        super().__init__(**{**palm_params('palm-tony'), **kwargs})


class PaLM8B(PaLM):
    def __init__(self, **kwargs):
        super().__init__(**{**palm_params('palm-8b'), **kwargs})


class PaLM62B(PaLM):
    def __init__(self, **kwargs):
        super().__init__(**{**palm_params('palm-62b'), **kwargs})


class PaLM540B(PaLM):
    def __init__(self, **kwargs):
        super().__init__(**{**palm_params('palm-540b'), **kwargs})
