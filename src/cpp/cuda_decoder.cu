#include "qec/types.hpp"

#include <cublas_v2.h>
#include <curand_kernel.h>

namespace qec {

__global__ void pack_syndrome_bits_kernel(const std::uint8_t* defects,
                                          float* tensor,
                                          std::size_t count) {
  const auto idx = blockIdx.x * blockDim.x + threadIdx.x;
  if (idx < count) {
    tensor[idx] = defects[idx] ? 1.0f : 0.0f;
  }
}

__global__ void init_curand_kernel(curandStatePhilox4_32_10_t* states,
                                   unsigned long long seed,
                                   std::size_t count) {
  const auto idx = blockIdx.x * blockDim.x + threadIdx.x;
  if (idx < count) {
    curand_init(seed, idx, 0, &states[idx]);
  }
}

extern "C" int qec_cuda_runtime_probe() {
  cublasHandle_t handle = nullptr;
  const auto status = cublasCreate(&handle);
  if (status != CUBLAS_STATUS_SUCCESS) {
    return static_cast<int>(status);
  }
  cublasDestroy(handle);
  return 0;
}

}  // namespace qec

