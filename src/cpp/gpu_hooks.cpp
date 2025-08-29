#include "qec/gpu_hooks.hpp"

namespace qec {

GpuBackendStatus gpu_backend_status() {
#ifdef QEC_ENABLE_CUDA
  return {true, "cuda", "CUDA hooks compiled; cuRAND/cuBLAS symbols are linked by CMake."};
#else
  return {false, "cpu", "Build with -DQEC_ENABLE_CUDA=ON to compile CUDA/cuBLAS/cuRAND hooks."};
#endif
}

}  // namespace qec

