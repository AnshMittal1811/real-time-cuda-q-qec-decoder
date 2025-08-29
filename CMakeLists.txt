cmake_minimum_required(VERSION 3.22)

project(real_time_cuda_q_qec_decoder
  VERSION 0.1.0
  LANGUAGES CXX)

option(QEC_ENABLE_CUDA "Build optional CUDA/cuBLAS/cuRAND decoder hooks" OFF)
option(QEC_BUILD_TESTS "Build C++ smoke tests" ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(qec_core
  src/cpp/surface_code.cpp
  src/cpp/baseline_decoder.cpp
  src/cpp/metrics.cpp
  src/cpp/gpu_hooks.cpp)

target_include_directories(qec_core PUBLIC include)
target_compile_options(qec_core PRIVATE
  $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>)

if(QEC_ENABLE_CUDA)
  enable_language(CUDA)
  find_package(CUDAToolkit REQUIRED)
  target_sources(qec_core PRIVATE src/cpp/cuda_decoder.cu)
  target_link_libraries(qec_core PUBLIC CUDA::cudart CUDA::curand CUDA::cublas)
  target_compile_definitions(qec_core PUBLIC QEC_ENABLE_CUDA=1)
endif()

add_executable(qec_benchmark src/cpp/main.cpp)
target_link_libraries(qec_benchmark PRIVATE qec_core)

if(QEC_BUILD_TESTS)
  enable_testing()
  add_executable(qec_smoke_test tests/cpp_smoke_test.cpp)
  target_link_libraries(qec_smoke_test PRIVATE qec_core)
  add_test(NAME qec_smoke_test COMMAND qec_smoke_test)
endif()

