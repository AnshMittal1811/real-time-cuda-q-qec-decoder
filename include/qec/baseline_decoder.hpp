#pragma once

#include "qec/types.hpp"

namespace qec {

class UnionFindLikeDecoder {
 public:
  DecodeResult decode(const SyndromeSample& sample) const;
};

}  // namespace qec

