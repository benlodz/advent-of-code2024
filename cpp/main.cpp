// #include <fmt/format.h>

#include <common/common.hpp>
#include <filesystem>
#include <tuple>

std::pair<std::filesystem::path, std::filesystem::path> getSampleAndInput() {
  namespace fs = std::filesystem;
  using std::string;

  fs::path current_path = std::filesystem::current_path();

  // This assumes you run from cpp/build directory
  // TODO: Maybe run a check that this is the correct path?
  current_path = current_path.parent_path().parent_path();
  auto input_path = current_path / "input";
  auto sample_path = current_path / "sample";

  return std::pair<fs::path, fs::path>(input_path, sample_path);
}

std::tuple<std::string, bool, bool> parse_arguments(s32 argc, char *argv[]) {
  using std::pair;
  using std::string;
  using std::tuple;

  argparse::ArgumentParser parser("AoC 2024: C++ Edition");

  pair<string, string> input_and_sample_path = getSampleAndInput();

  parser.add_description(
      "This will solve all puzzle inputs for Advent of Code 2024. Files should "
      "be placed in the input folder with the format of dayN_input.txt.");

  parser.add_argument("-i", "--input")
      .required()
      .default_value(input_and_sample_path.first)
      .help("Specify the path to the puzzle input.");

  parser.add_argument("-d", "--debug")
      .help("Specify whether to turn on debugging. Off by default")
      .flag();

  parser.add_argument("-s", "--samples")
      .help("Specify whether to turn on debugging. Off by default")
      .flag();

  try {
    parser.parse_args(argc, argv);
  } catch (const std::exception &err) {
    std::cerr << "Caught exception when trying to parse args: " << err.what()
              << std::endl;
    throw std::runtime_error("Failed to parse arguments!");
  }

  std::string input_path = parser.get<std::string>("--input");
  bool debug = parser.get<bool>("--debug");
  bool samples = parser.get<bool>("--samples");
  return std::tuple(input_path, debug, samples);
}

std::filesystem::path get_full_path(std::filesystem::path input_path, s8 day,
                                    bool samples) {
  return (input_path / ("day" + std::to_string(day) + "_input.txt"));
}

int main(int argc, char *argv[]) {
  auto [input_path, debug, samples] = parse_arguments(argc, argv);
  auto logger = getLogger("MAIN", debug);

  if (debug) logger->debug("Debugging is on!");
  if (samples) logger->debug("Running samples!");
  logger->debug("Input path: {}", input_path);

  // C++ doesn't support introspection so we have to call each function.
  day1_solve(get_full_path(input_path, 1, false), debug);
  day2_solve(get_full_path(input_path, 2, false), debug);
  return 0;
}
