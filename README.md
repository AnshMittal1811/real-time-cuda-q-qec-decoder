# Real-Time CUDA-Q Quantum Error Correction Decoder

GPU-accelerated surface-code quantum error correction decoder prototype using a
CUDA-Q-ready data model, C++17 runtime, optional cuBLAS/cuRAND hooks, and a PyTorch
transformer decoder.

> Timeline: May 2025-Dec 2025  
> Target result: 2.3x median decode-latency reduction vs. a CPU baseline after running
> the optional GPU/CUDA-Q path on a CUDA workstation.

## What This Implements

This repository is a runnable implementation scaffold for a real-time QEC decoding loop:

```text
surface-code syndrome stream
        |
        v
detector-level sample schema
        |
        v
C++17 ring-buffer-friendly decoder runtime
        |
        v
PyTorch transformer decoder / CPU baseline
        |
        v
correction vector + logical-risk metrics
```

The checked-in path is detector-level and CPU-verifiable so it can run on development
machines without CUDA-Q. The CUDA hooks and documentation show where CUDA-Q QEC sampling,
cuRAND noise generation, cuBLAS-backed dense inference, and TorchScript/LibTorch inference
fit into the production GPU path.

## Repository Layout

```text
.
├── CMakeLists.txt                  # C++17 build with optional CUDA mode
├── configs/default.yaml            # Default experiment configuration
├── docs/architecture.md            # Data flow and runtime architecture
├── docs/timeline.md                # May-Dec 2025 milestone history
├── include/qec                     # C++ public headers
├── src/cpp                         # C++ simulator, baseline, metrics, CUDA hook
├── src/python/qec_decoder          # Python simulator, transformer, training, export
├── tests                           # Python and C++ smoke tests
└── benchmarks/reference_result.json
```

## Core Implementation Details

### Surface-Code Representation

The prototype uses a detector-level rotated surface-code abstraction:

- `distance`: odd code distance, default `5`
- `rounds`: repeated stabilizer-measurement rounds, default `5`
- `plaquettes_per_round = 2 * distance * (distance - 1)`
- `syndrome_size = plaquettes_per_round * rounds`
- `correction_size = 2 * distance * distance`

Each sample stores:

```json
{
  "distance": 5,
  "rounds": 5,
  "physical_error_rate": 0.005,
  "defects": [0, 1, 0],
  "correction": [0, 0, 1],
  "logical_error": false
}
```

The local simulator generates reproducible syndrome bits with a seeded random source and a
small hook-error model. A CUDA-Q workstation can replace the local generator with CUDA-Q
QEC surface-code sampling while preserving the same downstream schema.

### Decoder Paths

The repo contains two decoder paths:

1. **CPU baseline:** deterministic union-find-like local pairing heuristic in C++17 and
   Python. This is the reference path for correctness checks and latency comparison.
2. **Neural decoder:** compact PyTorch transformer that maps syndrome bits to correction
   logits. It can be exported to TorchScript for a C++ inference path.

The transformer is intentionally compact:

- input projection from syndrome bit to hidden width
- learned positional embedding over detector indices
- transformer encoder stack
- pooled correction head
- `BCEWithLogitsLoss` over correction bits

### GPU Path

The optional CUDA build mode is enabled with:

```bash
cmake -S . -B build-cuda -DQEC_ENABLE_CUDA=ON
cmake --build build-cuda
```

That path links:

- `CUDA::cudart`
- `CUDA::curand`
- `CUDA::cublas`

The included CUDA file provides:

- syndrome bit packing into float tensors
- Philox cuRAND state initialization
- cuBLAS runtime probe

On a full CUDA-Q workstation, the intended optimized path is:

1. Generate syndrome rounds with CUDA-Q QEC surface-code sampling.
2. Keep syndrome tensors GPU-resident.
3. Use CUDA kernels for bit packing and syndrome-delta preprocessing.
4. Run the exported PyTorch model through LibTorch/TorchScript or TensorRT.
5. Use CUDA events for GPU section timing and wall-clock timing for end-to-end latency.

## Quick Start

Build and run the C++ baseline:

```bash
cmake -S . -B build -DQEC_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
./build/qec_benchmark --distance 5 --rounds 5 --p 0.005 --shots 1024
```

Run the Python simulator and benchmark:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
python3 -m pytest
python3 -m qec_decoder.benchmark --distance 5 --rounds 5 --p 0.005 --shots 1024
```

Train and export the transformer decoder:

```bash
pip install -e .[ml]
qec-train --distance 5 --rounds 5 --p 0.005 --shots 4096 --epochs 5
qec-export --checkpoint benchmarks/decoder.local.pt --output benchmarks/decoder.local.ts
```

## Benchmark Methodology

Report all latency numbers with:

- backend name
- code distance
- number of syndrome rounds
- physical error rate
- shots
- p50 decode latency
- p95 decode latency
- p99 decode latency
- logical failures

The headline speedup should be computed as:

```text
speedup = cpu_baseline_p50_decode_ms / gpu_decoder_p50_decode_ms
```

The target project claim is a **2.3x median decode-latency reduction vs. CPU baseline**.
This repo includes the benchmark harness and schema; the claim should be validated on the
same GPU workstation used for the CUDA-Q/cuBLAS/cuRAND run.

## CI/CD Benchmark Drift

GitHub Actions runs a drift-based CI pipeline on pushes, pull requests, and manual
dispatches:

- build the C++17 decoder
- run C++ and Python tests
- run the C++ baseline benchmark
- run the Python decoder benchmark
- compare C++ benchmark drift against `benchmarks/cpu_baseline.json`
- compare Python decoder latency against the current C++ decoder result
- upload JSON and Markdown drift artifacts
- write the drift tables to the GitHub Actions job summary

The drift gate is configurable from the workflow dispatch form:

| Setting | Default | Meaning |
|---|---:|---|
| `shots` | `512` | Number of benchmark samples in CI |
| `fail_on_drift` | `false` | If `true`, fail CI when drift exceeds thresholds |
| `LATENCY_DRIFT_THRESHOLD` | `0.35` | 35% relative latency regression threshold |
| `FAILURE_RATE_DRIFT_THRESHOLD` | `0.02` | 2 percentage point logical-failure regression threshold |

The default mode reports drift without failing because GitHub-hosted runner latency can
vary. For release branches or self-hosted GPU runners, set `fail_on_drift=true`.

## Local Verification Snapshot

This repository was verified on a CPU-only development machine with:

```bash
python3 -m compileall src/python tests
PYTHONPATH=src/python python3 -m unittest discover -s tests
cmake -S . -B build -DQEC_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
./build/qec_benchmark --distance 5 --rounds 5 --p 0.005 --shots 256 --seed 1337
PYTHONPATH=src/python python3 -m qec_decoder.benchmark --distance 5 --rounds 5 --p 0.005 --shots 256 --seed 1337
```

Observed local CPU-only p50 decode latency with `1024` shots:

| Backend | p50 decode latency |
|---|---:|
| C++17 CPU baseline | `0.000401 ms` |
| Python CPU baseline | `0.002861 ms` |

The GPU/CUDA-Q build was not run on this machine because `nvcc` is not installed.

## Timeline

| Month | Milestone | Implementation |
|---|---|---|
| May 2025 | Scope and baseline | Surface-code schema, CPU baseline plan |
| June 2025 | Syndrome generation | Reproducible detector-level dataset generation |
| July 2025 | PyTorch decoder | Transformer model, training loop, TorchScript export |
| August 2025 | C++17 runtime | CMake build, C++ simulator, decoder, latency metrics |
| September 2025 | GPU hooks | Optional CUDA/cuRAND/cuBLAS compilation path |
| October 2025 | Evaluation | Python and C++ benchmark harnesses |
| November 2025 | Demo hardening | Scripts, configs, architecture documentation |
| December 2025 | Final package | README, timeline, GitHub-ready repository |

## Resume Summary

Built a real-time GPU-oriented surface-code quantum error correction decoder using
CUDA-Q-ready syndrome generation, PyTorch transformer inference, C++17 benchmarking, and
optional cuBLAS/cuRAND CUDA hooks, with a benchmark harness designed to validate a 2.3x
median latency reduction against a CPU baseline.
