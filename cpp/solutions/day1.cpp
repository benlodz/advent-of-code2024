#include <common/common.hpp>

std::pair<std::vector<s32>, std::vector<s32>> getLists(
    std::vector<std::string> &lines) {
  // In order to solve day 1's problems, we need to split the input file s32o
  // two separate lists. Our lists are just numbers so we can go ahead and
  // create an array of numbers for every list.

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
  // In the first part of the problem, we need to take the smallest possible
  // number from both lists, and then calculate the distance between them.
  //
  // Example:
  // 3   4
  // 4   3
  // 2   5
  // 1   3
  // 3   9
  // 3   3
  // In this scenario, we would take 1 from the first list and take 3 from the
  // second. The distance between them would be |1 - 3| = 2. We then repeat
  // this process. This is easily done by using a min-heap and then popping
  // from both of them.

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
    score += cnt[n1];
  }
  return score;
}

void day1_solve(const std::string file_path) {
  logger = getLogger("Day 1 Logger");

  auto lines = getLines(file_path.c_str());
  auto lists = getLists(lines);

  auto distance = getDistance(lists);
  logger->info("The distance score between the two lists is: {}", distance);
  auto similarity_score = getSimilarity(lists);
  logger->info("The similarity score calculated between the two lists is: {}",
               similarity_score);
}
