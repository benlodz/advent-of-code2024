#ifndef COMMON_H
#define COMMON_H

// clang-format off
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>

#include <algorithm>
#include <argparse/argparse.hpp>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#include <regex>
// clang-format on

using u8 = std::uint8_t;
using u16 = std::uint16_t;
using u32 = std::uint32_t;
using u64 = std::uint64_t;
using usz = std::size_t;

using s8 = std::int8_t;
using s16 = std::int16_t;
using s32 = std::int32_t;
using s64 = std::int64_t;

std::shared_ptr<spdlog::logger> logger;

std::shared_ptr<spdlog::logger> getLogger(const std::string &name) {
  auto logger = spdlog::stdout_color_mt(name);
  return logger;
}

std::vector<std::string> getLines(const char *file_path) {
  using namespace std;

  ifstream file;
  vector<string> lines;
  string line;

  // Error handling.
  file.exceptions(ifstream::badbit | ifstream::failbit);

  try {
    file.open(file_path);
    while (getline(file, line)) {
      lines.push_back(line);
    }
  } catch (ifstream::failure e) {
    runtime_error("Failed to read the file!");
  }

  return lines;
}

#endif
