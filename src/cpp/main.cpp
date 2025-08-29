#include "qec/baseline_decoder.hpp"
#include "qec/gpu_hooks.hpp"
#include "qec/metrics.hpp"
#include "qec/surface_code.hpp"

#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

int parse_int(const char* value, const char* name) {
  char* end = nullptr;
  const long parsed = std::strtol(value, &end, 10);
  if (end == value || *end != '\0') {
    throw std::invalid_argument(std::string("invalid integer for ") + name);
  }
  return static_cast<int>(parsed);
}

double parse_double(const char* value, const char* name) {
  char* end = nullptr;
  const double parsed = std::strtod(value, &end);
  if (end == value || *end != '\0') {
    throw std::invalid_argument(std::string("invalid float for ") + name);
  }
  return parsed;
}

}  // namespace

int main(int argc, char** argv) {
  qec::DecoderConfig config;
  std::size_t shots = 256;

  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg == "--distance" && i + 1 < argc) {
      config.distance = parse_int(argv[++i], "--distance");
    } else if (arg == "--rounds" && i + 1 < argc) {
      config.rounds = parse_int(argv[++i], "--rounds");
    } else if (arg == "--p" && i + 1 < argc) {
      config.physical_error_rate = parse_double(argv[++i], "--p");
    } else if (arg == "--shots" && i + 1 < argc) {
      shots = static_cast<std::size_t>(parse_int(argv[++i], "--shots"));
    } else if (arg == "--seed" && i + 1 < argc) {
      config.seed = static_cast<std::uint64_t>(parse_int(argv[++i], "--seed"));
    } else if (arg == "--help") {
      std::cout << "qec_benchmark [--distance 5] [--rounds 5] [--p 0.005]"
                   " [--shots 256] [--seed 1337]\n";
      return 0;
    } else {
      throw std::invalid_argument("unknown or incomplete argument: " + arg);
    }
  }

  qec::SurfaceCodeSimulator simulator(config);
  qec::UnionFindLikeDecoder decoder;
  std::vector<double> decode_latencies;
  decode_latencies.reserve(shots);

  std::size_t failures = 0;
  for (std::size_t shot = 0; shot < shots; ++shot) {
    auto sample = simulator.sample();
    double elapsed_ms = 0.0;
    {
      qec::ScopedTimer timer(elapsed_ms);
      const auto result = decoder.decode(sample);
      failures += (sample.logical_error && result.logical_risk > 0.5) ? 1 : 0;
    }
    decode_latencies.push_back(elapsed_ms);
  }

  const auto gpu_status = qec::gpu_backend_status();
  std::cout << "{\n";
  std::cout << "  \"backend\": \"" << gpu_status.backend << "\",\n";
  std::cout << "  \"gpu_available\": " << (gpu_status.available ? "true" : "false") << ",\n";
  std::cout << "  \"distance\": " << config.distance << ",\n";
  std::cout << "  \"rounds\": " << config.rounds << ",\n";
  std::cout << "  \"physical_error_rate\": " << config.physical_error_rate << ",\n";
  const auto summary = qec::summarize_latencies(decode_latencies);
  std::cout << "  \"shots\": " << shots << ",\n";
  std::cout << "  \"logical_failures\": " << failures << ",\n";
  std::cout << "  \"mean_decode_ms\": " << summary.mean_ms << ",\n";
  std::cout << "  \"p50_decode_ms\": " << summary.p50_ms << ",\n";
  std::cout << "  \"p95_decode_ms\": " << summary.p95_ms << ",\n";
  std::cout << "  \"p99_decode_ms\": " << summary.p99_ms << "\n";
  std::cout << "}\n";
  return 0;
}

