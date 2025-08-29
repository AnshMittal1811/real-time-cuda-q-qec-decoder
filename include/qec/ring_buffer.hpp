#pragma once

#include <cstddef>
#include <stdexcept>
#include <utility>
#include <vector>

namespace qec {

template <typename T>
class RingBuffer {
 public:
  explicit RingBuffer(std::size_t capacity) : buffer_(capacity) {
    if (capacity == 0) {
      throw std::invalid_argument("ring buffer capacity must be positive");
    }
  }

  void push(T value) {
    buffer_[write_index_] = std::move(value);
    write_index_ = (write_index_ + 1) % buffer_.size();
    if (size_ < buffer_.size()) {
      ++size_;
    }
  }

  const T& newest(std::size_t offset = 0) const {
    if (offset >= size_) {
      throw std::out_of_range("ring buffer offset outside populated range");
    }
    const auto index = (write_index_ + buffer_.size() - 1 - offset) % buffer_.size();
    return buffer_[index];
  }

  std::size_t size() const { return size_; }
  std::size_t capacity() const { return buffer_.size(); }
  bool full() const { return size_ == buffer_.size(); }

 private:
  std::vector<T> buffer_;
  std::size_t write_index_ = 0;
  std::size_t size_ = 0;
};

}  // namespace qec

