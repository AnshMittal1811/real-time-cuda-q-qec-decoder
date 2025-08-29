#pragma once

#include <string>

namespace qec {

struct GpuBackendStatus {
  bool available = false;
  std::string backend = "cpu";
  std::string detail;
};

GpuBackendStatus gpu_backend_status();

}  // namespace qec

