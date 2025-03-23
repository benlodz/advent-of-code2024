// #include <fmt/format.h>

#include <common/common.hpp>
#include <filesystem>
#include <tuple>

std::pair<std::filesystem::path, std::filesystem::path>
getInputandSamplePaths() {
  namespace fs = std::filesystem;
  using std::string;

  fs::path current_path = std::filesystem::current_path();

  // This assumes you run from cpp/build directory
  // TODO: Maybe run a check that this is the correct path?
  current_path = current_path.parent_path().parent_path();
  auto input_path = current_path / "input";
  auto sample_path = current_path / "samples";

  return std::pair<fs::path, fs::path>(input_path, sample_path);
}

std::tuple<std::string, bool, bool> parse_arguments(s32 argc, char *argv[]) {
  using std::pair;
  using std::string;
  using std::tuple;
  namespace fs = std::filesystem;

  argparse::ArgumentParser parser("AoC 2024: C++ Edition");

  parser.add_description(
      "This will solve all puzzle inputs for Advent of Code 2024. Files should "
      "be placed in the input folder with the format of dayN_input.txt.");

  parser.add_argument("-i", "--input")
      .help("Specify the path to the puzzle input.");

  parser.add_argument("-d", "--debug")
      .help("Specify whether to turn on debugging. Off by default")
      .flag();

  parser.add_argument("-s", "--samples")
      .help("Specify whether to use samples. Off by default")
      .flag();

  try {
    parser.parse_args(argc, argv);
  } catch (const std::exception &err) {
    std::cerr << "Caught exception when trying to parse args: " << err.what()
              << std::endl;
    throw std::runtime_error("Failed to parse arguments!");
  }

  auto [input_path, sample_path] = getInputandSamplePaths();
  bool debug = parser.get<bool>("--debug");
  bool samples = parser.get<bool>("--samples");

  std::string final_path;
  if (parser.is_used("--input")) {
    throw std::runtime_error("Haven't implemented this yet...");
  } else if (samples) {
    final_path = sample_path;
  } else {
    final_path = input_path;
  }

  return std::tuple(final_path, debug, samples);
}

std::filesystem::path get_full_path(std::filesystem::path input_path, s8 day,
                                    bool samples) {
  if (samples) {
    return (input_path / ("day" + std::to_string(day) + "_sample.txt"));
  } else {
    return (input_path / ("day" + std::to_string(day) + "_input.txt"));
  }
}

int main(int argc, char *argv[]) {
  auto [input_path, debug, samples] = parse_arguments(argc, argv);
  auto logger = getLogger("MAIN", debug);

  if (debug) logger->debug("Debugging is on!");
  if (samples) logger->debug("Running samples!");
  logger->debug("Input path: {}", input_path);

  // C++ doesn't support introspection so we have to call each function.
  day1_solve(get_full_path(input_path, 1, samples), debug);
  day2_solve(get_full_path(input_path, 2, samples), debug);
  day3_solve(get_full_path(input_path, 3, samples), debug);
  return 0;
}
