#pragma once

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace qec {

struct DecoderConfig {
  int distance = 5;
  int rounds = 5;
  double physical_error_rate = 0.005;
  std::uint64_t seed = 1337;
};

struct SyndromeSample {
  int distance = 0;
  int rounds = 0;
  std::vector<std::uint8_t> defects;
  std::vector<std::uint8_t> correction;
  bool logical_error = false;
};

struct DecodeResult {
  std::vector<std::uint8_t> correction;
  double logical_risk = 0.0;
  std::size_t active_defects = 0;
};

inline std::size_t plaquettes_per_round(int distance) {
  return static_cast<std::size_t>(2 * distance * (distance - 1));
}

inline std::size_t syndrome_size(int distance, int rounds) {
  return plaquettes_per_round(distance) * static_cast<std::size_t>(rounds);
}

inline std::size_t correction_size(int distance) {
  return static_cast<std::size_t>(2 * distance * distance);
}

}  // namespace qec

