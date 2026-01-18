from __future__ import annotations

import argparse
from pathlib import Path

from qec_decoder.model import TransformerQECDecoder, require_torch, torch


def export_tensorrt(model: torch.nn.Module, output_path: Path) -> None:
    """Placeholder for TensorRT engine generation using the TRT Python API."""
    print(f"Generating TensorRT engine: {output_path}")
    # In a real implementation, this would use the tensorrt library
    # to build a serialized engine from the ONNX or TorchScript model.
    # See: 250DaysStraight/328_tensorrt_infer
    output_path.write_text("DUMMY TENSORRT ENGINE DATA")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a trained decoder to optimized formats.")
    parser.add_argument("--checkpoint", type=Path, default=Path("benchmarks/decoder.local.pt"))
    parser.add_argument("--output", type=Path, default=Path("benchmarks/decoder.local.ts"))
    parser.add_argument("--format", type=str, choices=["torchscript", "tensorrt"], default="torchscript")
    args = parser.parse_args()

    require_torch()
    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    model = TransformerQECDecoder(
        checkpoint["syndrome_size"],
        checkpoint["correction_size"],
        precision=checkpoint.get("precision", "fp32")
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "torchscript":
        example = torch.zeros(1, checkpoint["syndrome_size"], dtype=torch.float32)
        traced = torch.jit.trace(model, example)
        traced.save(str(args.output))
        print(f"exported TorchScript decoder to {args.output}")
    elif args.format == "tensorrt":
        export_tensorrt(model, args.output.with_suffix(".engine"))


if __name__ == "__main__":
    main()

