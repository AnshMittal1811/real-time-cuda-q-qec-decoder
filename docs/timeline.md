# Timeline

## May 2025: Scope and Baseline

- Defined a rotated surface-code detector-level representation.
- Selected distance 5, five syndrome rounds, and configurable physical error rate as the
  default benchmark target.
- Chose a deterministic union-find-like CPU decoder as the local correctness and latency
  baseline.

## June 2025: Syndrome Generation

- Added reproducible syndrome generation with fixed seeds.
- Added JSONL dataset export for training and benchmark reproducibility.

## July 2025: PyTorch Decoder

- Added a compact transformer decoder.
- Added training and TorchScript export entrypoints.

## August 2025: C++17 Runtime

- Added C++17 simulator, baseline decoder, and benchmark executable.
- Added smoke tests and CMake build configuration.

## September 2025: GPU Hooks

- Added optional CUDA build mode.
- Added cuRAND state initialization and cuBLAS runtime probe stubs for workstation builds.

## October 2025: Evaluation

- Added Python and C++ benchmark paths.
- Standardized p50, p95, p99, throughput, and logical-failure metrics.

## November 2025: Demo Hardening

- Added scripts for reproducible local benchmark runs.
- Added architecture documentation and configuration files.

## December 2025: Final Package

- Consolidated implementation notes into the README.
- Prepared the repository for GitHub publication.

