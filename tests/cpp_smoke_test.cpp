#include "qec/baseline_decoder.hpp"
#include "qec/ring_buffer.hpp"
#include "qec/surface_code.hpp"

#include <cassert>
#include <iostream>

int main() {
  qec::DecoderConfig config;
  config.distance = 5;
  config.rounds = 5;
  config.physical_error_rate = 0.01;
  config.seed = 7;

  qec::SurfaceCodeSimulator simulator(config);
  const auto sample = simulator.sample();
  assert(sample.defects.size() == qec::syndrome_size(config.distance, config.rounds));
  assert(sample.correction.size() == qec::correction_size(config.distance));

  qec::UnionFindLikeDecoder decoder;
  const auto decoded = decoder.decode(sample);
  assert(decoded.correction.size() == qec::correction_size(config.distance));

  qec::RingBuffer<qec::SyndromeSample> buffer(2);
  buffer.push(sample);
  buffer.push(simulator.sample());
  buffer.push(simulator.sample());
  assert(buffer.full());
  assert(buffer.newest().defects.size() == qec::syndrome_size(config.distance, config.rounds));

  std::cout << "cpp smoke test passed\n";
  return 0;
}
