#include <common/common.hpp>

static std::shared_ptr<spdlog::logger> logger;

std::string processLine(std::string line) {
  using namespace std;

  // logger->debug("size of string {}", line.size());
  s32 i{0};
  s8 do_offset{4};
  s8 dont_offset{7};
  bool enabled = true;
  s32 start{0};
  stringstream res;

  while (i < (line.size() - dont_offset)) {
    if ((enabled) && (line.substr(i, dont_offset) == "don't()")) {
      enabled = false;
    } else if ((!enabled) && (line.substr(i, do_offset) == "do()")) {
      enabled = true;
    }

    if (enabled) {
      res << line[i];
    }
    i++;
  }
  return res.str();
}

s32 getUncorruptedMul(std::string line) {
  using namespace std;
  regex pattern(R"(mul\((\d{1,3}),(\d{1,3})\))");

  sregex_iterator it(line.begin(), line.end(), pattern);
  sregex_iterator end;

  vector<int> products;

  while (it != end) {
    // logger->debug("x: {}\ty: {}", (*it)[1].str(), (*it)[2].str());
    products.push_back(stoi((*it)[1]) * stoi((*it)[2]));
    it++;
  }

  return accumulate(products.begin(), products.end(), 0);
}

s32 getEnabledMul(std::string line) {
  using namespace std;
  string enabled_line = processLine(line);
  return getUncorruptedMul(enabled_line);
}

void day3_solve(const std::string& file_name, bool debug) {
  using namespace std;
  logger = getLogger("day3", debug);
  vector<string> lines = getLines(file_name);

  string line = accumulate(lines.begin() + 1, lines.end(), lines[0]);

  s32 uncorrupted_mul = getUncorruptedMul(line);
  logger->info("For part 1, the sum of our uncorrupted mull commands is: {}",
               uncorrupted_mul);
  s32 enabled_mul = getEnabledMul(line);
  logger->info("For part 2, the sum of the enabled mull commands is: {}",
               enabled_mul);
}
