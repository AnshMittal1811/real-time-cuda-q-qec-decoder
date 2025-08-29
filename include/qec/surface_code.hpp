#pragma once

#include "qec/types.hpp"

#include <random>
#include <vector>

namespace qec {

class SurfaceCodeSimulator {
 public:
  explicit SurfaceCodeSimulator(DecoderConfig config);

  SyndromeSample sample();
  std::vector<SyndromeSample> batch(std::size_t shots);

 private:
  DecoderConfig config_;
  std::mt19937_64 rng_;
  std::bernoulli_distribution defect_dist_;
  std::bernoulli_distribution hook_error_dist_;

  bool boundary_logical_event(const std::vector<std::uint8_t>& defects) const;
};

}  // namespace qec

