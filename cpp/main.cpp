#include <common/common.hpp>
#include <filesystem>

std::pair<std::string, std::string> getSampleAndInput() {
  using std::string;
  string current_path = std::filesystem::current_path();
  logger->debug("Found running path: {}", current_path);

  string suffix = "/cpp/main.cpp";
  string root_path =
      current_path.substr(0, current_path.size() - suffix.size());

  logger->debug("Root Path: {}", root_path);

  string input_path = root_path + "/input";
  string sample_path = root_path + "/sample";
  logger->debug("Input path: {}\nSample path: {}", input_path, sample_path);
  return std::pair<std::string, std::string>(input_path, sample_path);
}
std::string parse_arguments(s32 argc, char *argv[]) {
  using std::pair;
  using std::string;

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

  try {
    parser.parse_args(argc, argv);
  } catch (const std::exception &err) {
    logger->critical("An error occurred while parsing arguments: {}",
                     err.what());
    throw;
  }

  

  std::string input = parser.get<std::string>("--input");
  return input;
}

int main(int argc, char *argv[]) {
