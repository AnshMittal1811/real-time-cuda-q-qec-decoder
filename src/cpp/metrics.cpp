#include "qec/metrics.hpp"

#include <algorithm>
#include <iomanip>
#include <numeric>
#include <sstream>

namespace qec {

ScopedTimer::ScopedTimer(double& output_ms)
    : output_ms_(output_ms), start_(std::chrono::steady_clock::now()) {}

ScopedTimer::~ScopedTimer() {
  const auto stop = std::chrono::steady_clock::now();
  output_ms_ = std::chrono::duration<double, std::milli>(stop - start_).count();
}

LatencySummary summarize_latencies(std::vector<double> values) {
  LatencySummary summary;
  if (values.empty()) {
    return summary;
  }

  std::sort(values.begin(), values.end());
  const auto percentile = [&](double p) {
    const auto rank = static_cast<std::size_t>((p / 100.0) * static_cast<double>(values.size() - 1));
    return values[rank];
  };

  summary.mean_ms = std::accumulate(values.begin(), values.end(), 0.0) /
                    static_cast<double>(values.size());
  summary.p50_ms = percentile(50.0);
  summary.p95_ms = percentile(95.0);
  summary.p99_ms = percentile(99.0);
  return summary;
}

std::string to_json(const LatencySummary& summary, std::size_t shots, std::size_t failures) {
  std::ostringstream out;
  out << std::fixed << std::setprecision(6);
  out << "{\n";
  out << "  \"shots\": " << shots << ",\n";
  out << "  \"logical_failures\": " << failures << ",\n";
  out << "  \"mean_ms\": " << summary.mean_ms << ",\n";
  out << "  \"p50_ms\": " << summary.p50_ms << ",\n";
  out << "  \"p95_ms\": " << summary.p95_ms << ",\n";
  out << "  \"p99_ms\": " << summary.p99_ms << "\n";
  out << "}\n";
  return out.str();
}

}  // namespace qec

