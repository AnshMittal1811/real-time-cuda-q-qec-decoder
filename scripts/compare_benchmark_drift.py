#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path


LATENCY_KEYS = ("mean_decode_ms", "p50_decode_ms", "p95_decode_ms", "p99_decode_ms")


@dataclass(frozen=True)
class MetricDelta:
    key: str
    baseline: float
    current: float
    absolute_delta: float
    relative_delta: float
    threshold: float
    failed: bool


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative_delta(baseline: float, current: float) -> float:
    if math.isclose(baseline, 0.0, abs_tol=1e-12):
        return 0.0 if math.isclose(current, 0.0, abs_tol=1e-12) else math.inf
    return (current - baseline) / abs(baseline)


def failure_rate(payload: dict) -> float:
    shots = max(1, int(payload.get("shots", 1)))
    return float(payload.get("logical_failures", 0)) / float(shots)


def collect_deltas(
    baseline: dict,
    current: dict,
    latency_threshold: float,
    failure_rate_threshold: float,
) -> list[MetricDelta]:
    deltas: list[MetricDelta] = []
    for key in LATENCY_KEYS:
        base_value = float(baseline.get(key, 0.0))
        current_value = float(current.get(key, 0.0))
        rel = relative_delta(base_value, current_value)
        failed = rel > latency_threshold
        deltas.append(
            MetricDelta(
                key=key,
                baseline=base_value,
                current=current_value,
                absolute_delta=current_value - base_value,
                relative_delta=rel,
                threshold=latency_threshold,
                failed=failed,
            )
        )

    baseline_failure_rate = failure_rate(baseline)
    current_failure_rate = failure_rate(current)
    absolute_failure_delta = current_failure_rate - baseline_failure_rate
    deltas.append(
        MetricDelta(
            key="logical_failure_rate",
            baseline=baseline_failure_rate,
            current=current_failure_rate,
            absolute_delta=absolute_failure_delta,
            relative_delta=relative_delta(baseline_failure_rate, current_failure_rate),
            threshold=failure_rate_threshold,
            failed=absolute_failure_delta > failure_rate_threshold,
        )
    )
    return deltas


def format_percent(value: float) -> str:
    if math.isinf(value):
        return "inf"
    return f"{100.0 * value:.2f}%"


def render_markdown(label: str, baseline: dict, current: dict, deltas: list[MetricDelta]) -> str:
    failed = [delta for delta in deltas if delta.failed]
    lines = [
        f"## {label}",
        "",
        f"- Baseline backend: `{baseline.get('backend', 'unknown')}`",
        f"- Current backend: `{current.get('backend', 'unknown')}`",
        f"- Distance: `{current.get('distance')}`",
        f"- Rounds: `{current.get('rounds')}`",
        f"- Physical error rate: `{current.get('physical_error_rate')}`",
        f"- Shots: baseline `{baseline.get('shots')}`, current `{current.get('shots')}`",
        f"- Drift status: `{'failed' if failed else 'passed'}`",
        "",
        "| Metric | Baseline | Current | Abs Delta | Rel Delta | Threshold | Status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for delta in deltas:
        lines.append(
            "| {key} | {baseline:.9f} | {current:.9f} | {absolute:.9f} | {relative} | {threshold} | {status} |".format(
                key=delta.key,
                baseline=delta.baseline,
                current=delta.current,
                absolute=delta.absolute_delta,
                relative=format_percent(delta.relative_delta),
                threshold=format_percent(delta.threshold),
                status="regressed" if delta.failed else "ok",
            )
        )

    lines.append("")
    lines.append(
        "Latency drift uses relative change; logical failure drift uses absolute failure-rate change."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare QEC decoder benchmark drift.")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--label", default="QEC decoder benchmark drift")
    parser.add_argument("--latency-threshold", type=float, default=0.35)
    parser.add_argument("--failure-rate-threshold", type=float, default=0.02)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fail-on-drift", action="store_true")
    args = parser.parse_args()

    baseline = load_json(args.baseline)
    current = load_json(args.current)
    deltas = collect_deltas(
        baseline,
        current,
        latency_threshold=args.latency_threshold,
        failure_rate_threshold=args.failure_rate_threshold,
    )
    markdown = render_markdown(args.label, baseline, current, deltas)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(markdown)

    if args.fail_on_drift and any(delta.failed for delta in deltas):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

