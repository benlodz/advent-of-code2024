#include <common/common.hpp>

static std::shared_ptr<spdlog::logger> logger;

std::pair<std::vector<s32>, std::vector<s32>> getLists(
    std::vector<std::string> &lines) {
  std::vector<s32> l1(lines.size());
  std::vector<s32> l2(lines.size());

  s32 v1, v2;

  for (const auto &line : lines) {
    std::istringstream iss(line);
    // >> stops at whitespace
    if (!(iss >> v1 >> v2)) {
      std::runtime_error("Failed to extract characters!");
    } else {
      l1.push_back(v1);
      l2.push_back(v2);
    }
  }

  std::pair<std::vector<s32>, std::vector<s32>> lists(l1, l2);
  return lists;
}

s32 getDistance(const std::pair<std::vector<s32>, std::vector<s32>> &lists) {
  // Distance is calculated as absolute value of the difference
  // of the smallest values, so we just pop from the heap with our
  // formula.

  std::priority_queue<s32, std::vector<s32>, std::greater<s32>> h1;
  std::priority_queue<s32, std::vector<s32>, std::greater<s32>> h2;

  for (const auto &n : lists.first) {
    h1.push(n);
  }

  for (const auto &n : lists.second) {
    h2.push(n);
  }

  s32 distance{};
  // They're the same size so doesn't matter which one.
  while (!h1.empty()) {
    distance += abs(h1.top() - h2.top());
    h1.pop();
    h2.pop();
  }
  return distance;
}

s32 getSimilarity(std::pair<std::vector<s32>, std::vector<s32>> &lists) {
  // For part 2 of day 1, you have to calculate a "similarity score".
  // Essentially, for every number in the first list, how many times does it
  // occur in the second? We can accomplish this pretty easily with a hashmap.
  std::map<s32, s32> cnt;
  for (const auto n2 : lists.second) {
    cnt[n2] += 1;
  }
  s32 score{};
  for (const auto n1 : lists.first) {
    score += (cnt[n1] * n1);
  }
  return score;
}

void day1_solve(const std::string &file_path, bool debug) {
  logger = getLogger("Day 1", debug);

  auto lines = getLines(file_path.c_str());
  auto lists = getLists(lines);

  auto distance = getDistance(lists);
  logger->info("The distance score between the two lists is: {}", distance);
  auto similarity_score = getSimilarity(lists);
  logger->info("The similarity score calculated between the two lists is: {}",
               similarity_score);
}
