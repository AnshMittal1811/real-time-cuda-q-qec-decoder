from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError as exc:  # pragma: no cover - exercised only without optional deps
    torch = None
    nn = None
    _TORCH_IMPORT_ERROR = exc
else:
    _TORCH_IMPORT_ERROR = None


def require_torch() -> None:
    if torch is None:
        raise RuntimeError("PyTorch is required for model training/export. Install with: pip install -e .[ml]") from _TORCH_IMPORT_ERROR


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
    ) -> None:
        require_torch()
        super().__init__()
        self.syndrome_size = syndrome_size
        self.correction_size = correction_size
        self.precision = precision
        self.input_projection = nn.Linear(1, width)
        self.position = nn.Parameter(torch.zeros(1, syndrome_size, width))
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
        # In a real implementation, this would replace layers with quantized variants
        # e.g., using bitsandbytes or custom Triton kernels as explored in research.
        for name, module in self.named_modules():
            if isinstance(module, nn.Linear):
                module.precision = precision

    def forward(self, syndrome_bits):
        require_torch()
        x = syndrome_bits.float().view(syndrome_bits.shape[0], self.syndrome_size, 1)
        if self.precision == "fp16":
            x = x.half()
        x = self.input_projection(x) + self.position
        x = self.encoder(x)
        x = self.pool(x.transpose(1, 2)).squeeze(-1)
        return self.head(x)

