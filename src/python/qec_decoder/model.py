from __future__ import annotations
import math

try:
    import torch
    from torch import nn
    import torch.nn.functional as F
except ImportError as exc:  # pragma: no cover - exercised only without optional deps
    torch = None
    nn = None
    F = None
    _TORCH_IMPORT_ERROR = exc
else:
    _TORCH_IMPORT_ERROR = None


def require_torch() -> None:
    if torch is None:
        raise RuntimeError("PyTorch is required for model training/export. Install with: pip install -e .[ml]") from _TORCH_IMPORT_ERROR


class RingAttention(nn.Module):
    """
    Scalable block-wise attention for high-distance surface codes.
    See: 250DaysStraight/315_ring_attention_sim
    """
    def __init__(self, dim, heads=4, block_size=128):
        super().__init__()
        self.heads = heads
        self.block_size = block_size
        self.scale = 1.0 / math.sqrt(dim // heads)
        self.qkv = nn.Linear(dim, dim * 3)
        self.proj = nn.Linear(dim, dim)

    def forward(self, x):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.heads, C // self.heads).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        # Block-wise ring attention simulation
        out = torch.zeros_like(q)
        for i in range(0, N, self.block_size):
            q_block = q[:, :, i:i + self.block_size, :]
            attn = (q_block @ k.transpose(-2, -1)) * self.scale
            attn = attn.softmax(dim=-1)
            out[:, :, i:i + self.block_size, :] = attn @ v

        out = out.transpose(1, 2).reshape(B, N, C)
        return self.proj(out)


class TransformerQECDecoder(nn.Module if nn is not None else object):
    """Compact transformer decoder for syndrome-to-correction prediction."""

    def __init__(
        self,
        syndrome_size: int,
        correction_size: int,
        width: int = 128,
        layers: int = 4,
        heads: int = 4,
        dropout: float = 0.05,
        precision: str = "fp32",
        use_ring_attention: bool = False,
    ) -> None:
        require_torch()
        super().__init__()
        self.syndrome_size = syndrome_size
        self.correction_size = correction_size
        self.precision = precision
        self.input_projection = nn.Linear(1, width)
        self.position = nn.Parameter(torch.zeros(1, syndrome_size, width))
        
        if use_ring_attention:
            self.encoder = nn.ModuleList([
                RingAttention(width, heads=heads) for _ in range(layers)
            ])
        else:
            block = nn.TransformerEncoderLayer(
                d_model=width,
                nhead=heads,
                dim_feedforward=4 * width,
                dropout=dropout,
                batch_first=True,
                activation="gelu",
            )
            self.encoder = nn.TransformerEncoder(block, num_layers=layers)
            
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.head = nn.Sequential(
            nn.LayerNorm(width),
            nn.Linear(width, width),
            nn.GELU(),
            nn.Linear(width, correction_size),
        )

        if precision in ["int4", "fp8"]:
            self._apply_quantization(precision)

    def _apply_quantization(self, precision: str) -> None:
        """Apply quantization stubs for optimized inference backends."""
        print(f"Applying {precision} quantization stubs to model layers")
        for name, module in self.named_modules():
            if isinstance(module, nn.Linear):
                module.precision = precision

    def forward(self, syndrome_bits):
        require_torch()
        x = syndrome_bits.float().view(syndrome_bits.shape[0], self.syndrome_size, 1)
        if self.precision == "fp16":
            x = x.half()
        x = self.input_projection(x) + self.position
        
        if isinstance(self.encoder, nn.ModuleList):
            for layer in self.encoder:
                x = layer(x)
        else:
            x = self.encoder(x)
            
        x = self.pool(x.transpose(1, 2)).squeeze(-1)
        return self.head(x)

