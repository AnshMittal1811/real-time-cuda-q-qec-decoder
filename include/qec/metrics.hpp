#pragma once

#include <chrono>
#include <cstddef>
#include <string>
#include <vector>

namespace qec {

class ScopedTimer {
 public:
  explicit ScopedTimer(double& output_ms);
  ~ScopedTimer();

 private:
  double& output_ms_;
  std::chrono::steady_clock::time_point start_;
};

struct LatencySummary {
  double mean_ms = 0.0;
  double p50_ms = 0.0;
  double p95_ms = 0.0;
  double p99_ms = 0.0;
};

LatencySummary summarize_latencies(std::vector<double> values);
std::string to_json(const LatencySummary& summary, std::size_t shots, std::size_t failures);

}  // namespace qec

