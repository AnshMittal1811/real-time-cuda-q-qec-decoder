from __future__ import annotations

import argparse
import json
from pathlib import Path

from qec_decoder.geometry import SurfaceCodeGeometry
from qec_decoder.model import TransformerQECDecoder, require_torch, torch
from qec_decoder.simulator import generate_dataset


def _materialize_tensors(geometry: SurfaceCodeGeometry, p: float, shots: int, seed: int):
    require_torch()
    samples = list(generate_dataset(geometry, p, shots, seed))
    syndromes = torch.tensor([sample.defects for sample in samples], dtype=torch.float32)
    corrections = torch.tensor([sample.correction for sample in samples], dtype=torch.float32)
    return syndromes, corrections


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the transformer QEC decoder.")
    parser.add_argument("--distance", type=int, default=5)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--p", type=float, default=0.005)
    parser.add_argument("--shots", type=int, default=4096)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/decoder.local.pt"))
    args = parser.parse_args()

    require_torch()
    torch.manual_seed(args.seed)
    geometry = SurfaceCodeGeometry(args.distance, args.rounds)
    syndromes, corrections = _materialize_tensors(geometry, args.p, args.shots, args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TransformerQECDecoder(geometry.syndrome_size, geometry.correction_size).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4)
    loss_fn = torch.nn.BCEWithLogitsLoss()

    for epoch in range(args.epochs):
        permutation = torch.randperm(syndromes.shape[0])
        total_loss = 0.0
        for start in range(0, syndromes.shape[0], args.batch_size):
            idx = permutation[start : start + args.batch_size]
            x = syndromes[idx].to(device)
            y = corrections[idx].to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(x)
            loss = loss_fn(logits, y)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach().cpu())
        print(json.dumps({"epoch": epoch + 1, "loss": total_loss, "device": str(device)}))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "distance": args.distance,
            "rounds": args.rounds,
            "syndrome_size": geometry.syndrome_size,
            "correction_size": geometry.correction_size,
        },
        args.output,
    )
    print(f"saved checkpoint to {args.output}")


if __name__ == "__main__":
    main()

