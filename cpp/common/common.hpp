#ifndef COMMON_H
#define COMMON_H
#include <spdlog/spdlog.h>

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

using u8 = std::uint8_t;
using u16 = std::uint16_t;
using u32 = std::uint32_t;
using u64 = std::uint64_t;
using usz = std::size_t;

using s8 = std::int8_t;
using s16 = std::int16_t;
using s32 = std::int32_t;
using s64 = std::int64_t;

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

std::string parse_arguments(const std::string &program_name,
                            const std::string &program_desc, s32 argc,
                            char *argv[]) {
  argparse::ArgumentParser parser(program_name);

  parser.add_description(program_desc);

  // If no input file is provided, the sample will be used.
  parser.add_argument("-i", "--input")
      .default_value(program_name + "_sample.txt")
      .required()
      .help("Specify the input file.");

  try {
    parser.parse_args(argc, argv);
  } catch (const std::exception &err) {
    std::cerr << err.what() << std::endl;
  }

  std::string input = parser.get<std::string>("--input");
  return input;
}

#endif
