#include "qec/surface_code.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace qec {

SurfaceCodeSimulator::SurfaceCodeSimulator(DecoderConfig config)
    : config_(config),
      rng_(config.seed),
      defect_dist_(config.physical_error_rate),
      hook_error_dist_(std::min(0.5, std::pow(config.physical_error_rate, (config.distance + 1) / 2.0))) {
  if (config_.distance < 3 || config_.distance % 2 == 0) {
    throw std::invalid_argument("surface-code distance must be odd and >= 3");
  }
  if (config_.rounds <= 0) {
    throw std::invalid_argument("rounds must be positive");
  }
  if (config_.physical_error_rate < 0.0 || config_.physical_error_rate > 0.5) {
    throw std::invalid_argument("physical error rate must be in [0, 0.5]");
  }
}

SyndromeSample SurfaceCodeSimulator::sample() {
  SyndromeSample sample;
  sample.distance = config_.distance;
  sample.rounds = config_.rounds;
  sample.defects.resize(syndrome_size(config_.distance, config_.rounds));
  sample.correction.resize(correction_size(config_.distance));

  for (auto& defect : sample.defects) {
    defect = static_cast<std::uint8_t>(defect_dist_(rng_) ? 1 : 0);
  }

  for (std::size_t i = 0; i < sample.defects.size(); ++i) {
    if (sample.defects[i] == 0) {
      continue;
    }
    const auto target = (i * 1315423911ULL + static_cast<std::size_t>(config_.distance)) %
                        sample.correction.size();
    sample.correction[target] ^= 1;
  }

  sample.logical_error = boundary_logical_event(sample.defects) || hook_error_dist_(rng_);
  return sample;
}

std::vector<SyndromeSample> SurfaceCodeSimulator::batch(std::size_t shots) {
  std::vector<SyndromeSample> samples;
  samples.reserve(shots);
  for (std::size_t shot = 0; shot < shots; ++shot) {
    samples.push_back(sample());
  }
  return samples;
}

bool SurfaceCodeSimulator::boundary_logical_event(const std::vector<std::uint8_t>& defects) const {
  const auto per_round = plaquettes_per_round(config_.distance);
  int left_boundary_parity = 0;
  int right_boundary_parity = 0;

  for (int round = 0; round < config_.rounds; ++round) {
    const auto offset = static_cast<std::size_t>(round) * per_round;
    for (int row = 0; row < config_.distance - 1; ++row) {
      left_boundary_parity ^= defects[offset + static_cast<std::size_t>(row)];
      right_boundary_parity ^= defects[offset + per_round - 1 - static_cast<std::size_t>(row)];
    }
  }

  return left_boundary_parity == 1 && right_boundary_parity == 1;
}

}  // namespace qec

