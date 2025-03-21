#ifndef COMMON_H
#define COMMON_H

// clang-format off
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/fmt/ranges.h>

#include <algorithm>
#include <argparse/argparse.hpp>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#include <regex>
#include <functional>
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

inline std::shared_ptr<spdlog::logger> getLogger(const std::string& name,
                                                 bool debug) {
  auto logger = spdlog::stdout_color_mt(name);

  if (debug) logger->set_level(spdlog::level::debug);
  return logger;
}

inline std::vector<std::string> getLines(const std::string& file_name) {
  using namespace std;

  ifstream file;
  vector<string> lines;
  string line;

  // We need to expose the pointer for this to work properly.
  const char* file_path = file_name.c_str();

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

// Forward declare of all solve functions.
void day1_solve(const std::string& file_path, bool debug);
void day2_solve(const std::string& file_path, bool debug);

#endif
