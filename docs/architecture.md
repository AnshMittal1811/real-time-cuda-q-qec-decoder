# Architecture

The project is organized around a real-time detector-level decoding loop:

```text
CUDA-Q / CUDA-Q QEC simulation
        |
        v
Detector syndrome bits
        |
        v
C++17 ring buffer and CUDA preprocessing
        |
        v
PyTorch transformer exported to TorchScript/LibTorch
        |
        v
Correction mapper and logical-failure scorer
        |
        v
Latency and logical-error-rate reports
```

## Components

- `src/python/qec_decoder/simulator.py` generates reproducible detector-level syndrome
  samples for local development and training.
- `src/python/qec_decoder/model.py` defines the transformer decoder used for
  syndrome-to-correction prediction.
- `include/qec/ring_buffer.hpp` provides the bounded ingestion buffer used by the
  real-time syndrome stream.
- `src/cpp` contains the C++17 benchmark runtime and deterministic CPU baseline.
- `src/cpp/cuda_decoder.cu` is the optional CUDA build path for cuRAND/cuBLAS backed
  kernels. It is compiled only with `-DQEC_ENABLE_CUDA=ON`.
- `configs/default.yaml` captures the benchmark configuration that should be used for
  repeated runs.

## CUDA-Q Integration Point

The checked-in simulator is intentionally detector-level so the repo remains runnable on
machines without CUDA-Q. On a CUDA-Q workstation, replace the Python generator with CUDA-Q
QEC surface-code sampling and feed the same syndrome schema into the C++/PyTorch decoder.

The contract is:

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

## Latency Strategy

The benchmark separates syndrome generation, preprocessing, inference, postprocessing, and
end-to-end wall time. The C++ path reports p50, p95, and p99 decode latency so batch
throughput cannot hide real-time tail latency.
