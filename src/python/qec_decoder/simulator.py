from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from qec_decoder.geometry import SurfaceCodeGeometry


@dataclass(frozen=True)
class SyndromeSample:
    distance: int
    rounds: int
    physical_error_rate: float
    defects: list[int]
    correction: list[int]
    logical_error: bool


def _boundary_logical_event(geometry: SurfaceCodeGeometry, defects: list[int]) -> bool:
    left_parity = 0
    right_parity = 0
    for round_id in range(geometry.rounds):
        offset = round_id * geometry.plaquettes_per_round
        for row in range(geometry.distance - 1):
            left_parity ^= defects[offset + row]
            right_parity ^= defects[offset + geometry.plaquettes_per_round - 1 - row]
    return left_parity == 1 and right_parity == 1


def generate_sample(
    geometry: SurfaceCodeGeometry,
    physical_error_rate: float,
    rng: random.Random,
) -> SyndromeSample:
    if physical_error_rate < 0.0 or physical_error_rate > 0.5:
        raise ValueError("physical_error_rate must be in [0, 0.5]")

    defects = [
        1 if rng.random() < physical_error_rate else 0 for _ in range(geometry.syndrome_size)
    ]
    correction = [0 for _ in range(geometry.correction_size)]
    for index, bit in enumerate(defects):
        if bit:
            correction[(index * 1315423911 + geometry.distance) % geometry.correction_size] ^= 1

    hook_probability = min(0.5, math.pow(physical_error_rate, (geometry.distance + 1) / 2))
    logical_error = _boundary_logical_event(geometry, defects) or rng.random() < hook_probability
    return SyndromeSample(
        distance=geometry.distance,
        rounds=geometry.rounds,
        physical_error_rate=physical_error_rate,
        defects=defects,
        correction=correction,
        logical_error=logical_error,
    )


def generate_dataset(
    geometry: SurfaceCodeGeometry,
    physical_error_rate: float,
    shots: int,
    seed: int,
) -> Iterable[SyndromeSample]:
    rng = random.Random(seed)
    for _ in range(shots):
        yield generate_sample(geometry, physical_error_rate, rng)


def write_jsonl(samples: Iterable[SyndromeSample], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for sample in samples:
            handle.write(json.dumps(asdict(sample), separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate detector-level QEC syndrome samples.")
    parser.add_argument("--distance", type=int, default=5)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--p", type=float, default=0.005)
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/syndromes.local.jsonl"))
    args = parser.parse_args()

    geometry = SurfaceCodeGeometry(args.distance, args.rounds)
    samples = generate_dataset(geometry, args.p, args.shots, args.seed)
    write_jsonl(samples, args.output)
    print(f"wrote {args.shots} samples to {args.output}")


if __name__ == "__main__":
    main()

