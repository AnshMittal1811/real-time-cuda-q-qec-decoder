from __future__ import annotations

import argparse
from pathlib import Path

from qec_decoder.model import TransformerQECDecoder, require_torch, torch


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a trained decoder to TorchScript.")
    parser.add_argument("--checkpoint", type=Path, default=Path("benchmarks/decoder.local.pt"))
    parser.add_argument("--output", type=Path, default=Path("benchmarks/decoder.local.ts"))
    args = parser.parse_args()

    require_torch()
    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    model = TransformerQECDecoder(
        checkpoint["syndrome_size"],
        checkpoint["correction_size"],
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    example = torch.zeros(1, checkpoint["syndrome_size"], dtype=torch.float32)
    traced = torch.jit.trace(model, example)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    traced.save(str(args.output))
    print(f"exported TorchScript decoder to {args.output}")


if __name__ == "__main__":
    main()

