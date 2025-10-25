from __future__ import annotations

import argparse
import json
import random
import statistics
import time

from qec_decoder.geometry import SurfaceCodeGeometry
from qec_decoder.simulator import generate_sample


def union_find_like_decode(sample) -> tuple[list[int], float]:
    correction = [0 for _ in range(2 * sample.distance * sample.distance)]
    active = 0
    for index, bit in enumerate(sample.defects):
        if bit:
            active += 1
            correction[(index * 2654435761 + sample.rounds) % len(correction)] ^= 1
    risk = min(1.0, active / max(1, len(sample.defects)) * sample.distance)
    return correction, risk


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    index = int((p / 100.0) * (len(values) - 1))
    return values[index]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark the Python CPU decoder path.")
    parser.add_argument("--distance", type=int, default=5)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--p", type=float, default=0.005)
    parser.add_argument("--shots", type=int, default=512)
    parser.add_argument("--seed", type=int, default=1337)
    args = parser.parse_args()

    geometry = SurfaceCodeGeometry(args.distance, args.rounds)
    rng = random.Random(args.seed)
    latencies_ms: list[float] = []
    failures = 0

    for _ in range(args.shots):
        sample = generate_sample(geometry, args.p, rng)
        start = time.perf_counter_ns()
        _, risk = union_find_like_decode(sample)
        stop = time.perf_counter_ns()
        failures += int(sample.logical_error and risk > 0.5)
        latencies_ms.append((stop - start) / 1_000_000.0)

    print(
        json.dumps(
            {
                "backend": "python-cpu",
                "distance": args.distance,
                "rounds": args.rounds,
                "physical_error_rate": args.p,
                "shots": args.shots,
                "logical_failures": failures,
                "mean_decode_ms": statistics.fmean(latencies_ms),
                "p50_decode_ms": percentile(latencies_ms, 50),
                "p95_decode_ms": percentile(latencies_ms, 95),
                "p99_decode_ms": percentile(latencies_ms, 99),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

