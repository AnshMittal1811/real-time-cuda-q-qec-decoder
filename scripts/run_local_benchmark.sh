#!/usr/bin/env bash
set -euo pipefail

cmake -S . -B build -DQEC_BUILD_TESTS=ON
cmake --build build --target qec_benchmark qec_smoke_test
ctest --test-dir build --output-on-failure
./build/qec_benchmark --distance 5 --rounds 5 --p 0.005 --shots 1024 --seed 1337
PYTHONPATH=src/python python3 -m qec_decoder.benchmark --distance 5 --rounds 5 --p 0.005 --shots 1024 --seed 1337
