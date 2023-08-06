import torch
from einops import rearrange
from torch import nn, einsum
from torch.nn.modules.utils import _pair

__all__ = ['Attention', 'WindowAttention']


class Attention(nn.Module):
    def __init__(self, dim, num_heads=8, dim_head=None, drop=0.):
        super().__init__()
        dim_head = dim_head or dim // num_heads

        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

    def forward(self, x, mask=None):
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (nh d) -> b nh n d', nh=self.num_heads), (q, k, v))
        q = q * self.scale
        sim = einsum('b h i d, b h j d -> b h i j', q, k)  # h means nh
        # TODO: other mask types?
        if mask is not None:
            b, _, n, n = sim.shape
            assert mask.shape == (b, n, n), 'mask has incorrect dimensions'
            sim.masked_fill_(~mask, -torch.finfo(sim.dtype).max)
        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)


class WindowAttention(nn.Module):
    @staticmethod
    def double_step_seq(step1, len1, step2, len2):
        seq1 = torch.arange(0, step1 * len1, step1)
        seq2 = torch.arange(0, step2 * len2, step2)
        return (seq1[:, None] + seq2[None, :]).reshape(1, -1)

    def __init__(self, dim, window_size, num_heads, dim_head=None, drop=0.):
        super().__init__()
        dim_head = dim_head or dim // num_heads

        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

        wh, ww = _pair(window_size)
        self.ws = wh * ww
        self.relative_position_bias_table = nn.Parameter(torch.zeros((2 * wh - 1) * (2 * ww - 1), num_heads))
        rel_index_coords = self.double_step_seq(2 * ww - 1, wh, 1, ww)
        relative_position_index = rel_index_coords + rel_index_coords.T
        relative_position_index = relative_position_index.flip(1)
        relative_position_index = rearrange(relative_position_index, 'ws1 ws2-> (ws1 ws2)')
        self.register_buffer("relative_position_index", relative_position_index)

    def forward(self, x, mask=None):
        """
        Args:
            x: input features with shape of (num_windows*B, N, C)
            mask: (0/-inf) mask with shape of (num_windows, Wh*Ww, Wh*Ww) or None
        """
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (nh d) -> b nh n d', nh=self.num_heads), (q, k, v))
        q = q * self.scale
        sim = einsum('b h i d, b h j d -> b h i j', q, k)

        relative_position_bias = self.relative_position_bias_table[self.relative_position_index]
        relative_position_bias = rearrange(relative_position_bias, '(ws1 ws2) n-> 1 n ws1 ws2', ws1=self.ws)
        sim = sim + relative_position_bias
        if mask is not None:
            sim = rearrange(sim, '(b nw) nh n1 n2 -> b nw nh n1 n2', nw=mask.shape[0])
            mask = rearrange(mask, 'nw ws1 ws2 -> 1 nw 1 ws1 ws2')
            sim = sim + mask
            sim = rearrange(sim, 'b nw nh n1 n2 -> (b nw) nh n1 n2')

        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)
