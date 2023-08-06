import torch
from einops import rearrange
from torch import nn, einsum
from torch.nn.modules.utils import _pair

__all__ = ['Attention', 'WindowAttention', 'MultiQueryAttention']


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


class RotaryEmbedding(nn.Module):
    """rotary positional embedding.
    `RoFormer: Enhanced Transformer with Rotary Position Embedding
    <https://arxiv.org/abs/2104.09864>`_"""

    def __init__(self, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, max_seq_len):
        seq = torch.arange(max_seq_len, dtype=self.inv_freq.dtype)
        freqs = einsum("i , j -> i j", seq, self.inv_freq)
        return torch.cat((freqs, freqs), dim=-1)


class MultiQueryAttention(nn.Module):
    def __init__(self, dim, dim_head=None, num_heads=8, drop=0.):
        super().__init__()
        dim_head = dim_head or dim // num_heads
        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_q = nn.Linear(dim, inner_dim, bias=False)
        self.to_kv = nn.Linear(dim, dim_head * 2, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

        self.rotary_emb = RotaryEmbedding(dim_head)

        # for caching causal mask and rotary embeddings
        self.register_buffer("mask", None, persistent=False)
        self.register_buffer("pos_emb", None, persistent=False)

    def get_rotary_embedding(self, n):
        if self.pos_emb is not None and self.pos_emb.shape[-2] >= n:
            return self.pos_emb[:n]

        pos_emb = self.rotary_emb(n)
        self.register_buffer("pos_emb", pos_emb, persistent=False)
        return pos_emb

    @staticmethod
    def rotate_half(x):
        x = rearrange(x, "... (j d) -> ... j d", j=2)
        x1, x2 = x.unbind(dim=-2)
        return torch.cat((-x2, x1), dim=-1)

    def apply_rotary_pos_emb(self, pos, t):
        return (t * pos.cos()) + (self.rotate_half(t) * pos.sin())

    def get_mask(self, n):
        if self.mask is not None and self.mask.shape[-1] >= n:
            return self.mask[:n, :n]

        mask = torch.ones((n, n), dtype=torch.bool).triu(1)
        self.register_buffer("mask", mask, persistent=False)
        return mask

    def forward(self, x):
        q = self.to_q(x)
        k, v = self.to_kv(x).chunk(2, dim=-1)
        q = rearrange(q, "b n (nh d) -> b nh n d", nh=self.num_heads)

        positions = self.get_rotary_embedding(x.shape[1])
        q, k = map(lambda t: self.apply_rotary_pos_emb(positions, t), (q, k))

        q = q * self.scale
        sim = einsum('b h i d, b j d -> b h i j', q, k)  # h means nh
        causal_mask = self.get_mask(x.shape[1])
        sim = sim.masked_fill(causal_mask, -torch.finfo(sim.dtype).max)
        sim = sim - sim.amax(dim=-1, keepdim=True)
        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)
