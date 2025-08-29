#include "qec/baseline_decoder.hpp"

#include <algorithm>

namespace qec {

DecodeResult UnionFindLikeDecoder::decode(const SyndromeSample& sample) const {
  DecodeResult result;
  result.correction.assign(correction_size(sample.distance), 0);

  for (std::size_t i = 0; i < sample.defects.size(); ++i) {
    if (sample.defects[i] == 0) {
      continue;
    }
    ++result.active_defects;

    // Deterministic local pairing heuristic used as a lightweight CPU baseline.
    const auto target = (i * 2654435761ULL + static_cast<std::size_t>(sample.rounds)) %
                        result.correction.size();
    result.correction[target] ^= 1;
  }

  const double density = sample.defects.empty()
                             ? 0.0
                             : static_cast<double>(result.active_defects) /
                                   static_cast<double>(sample.defects.size());
  result.logical_risk = std::min(1.0, density * static_cast<double>(sample.distance));
  return result;
}

}  // namespace qec

