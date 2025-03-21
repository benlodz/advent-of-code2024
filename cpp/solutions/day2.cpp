#include <common/common.hpp>

static std::shared_ptr<spdlog::logger> logger;

template <typename Comparator>
bool isValidReportV1(const std::vector<s32> report, Comparator comp) {
  /*
  A report is valid if either it's ascending or descending,
  and the difference between two adjacent values fits the
  inequality of 1 <= diff <= 3
  */

  s32 diff{};
  for (int i{1}; i < report.size(); i++) {
    diff = abs(report[i] - report[i - 1]);

    if ((diff == 0) || (diff > 3) || (!comp(report[i - 1], report[i]))) {
      return false;
    }
  }
  return true;
}

s32 getValidReportCntV1(const std::vector<std::vector<s32>>& reports) {
  s32 valid_reports{};
  for (auto& report : reports) {
    if (isValidReportV1(report, std::greater<int>()) ||
        isValidReportV1(report, std::less<int>())) {
      valid_reports++;
    }
  }
  return valid_reports;
}

std::vector<std::vector<s32>> getReports(const std::vector<std::string> lines) {
  using namespace std;
  vector<vector<s32>> reports;

  for (const auto& line : lines) {
    vector<s32> report;
    istringstream iss(line);
    s32 n;

    while (iss >> n) report.push_back(n);
    reports.push_back(report);
  }
  return reports;
}

template <typename Comparator>
bool isValidReportV2(const std::vector<int>& report, Comparator comp) {
  using namespace std;
  // In this scenario, we can tolerate one bad report

  s8 i = 0, j = 1;
  s8 N = report.size();
  s32 diff{};

  while (j < N) {
    diff = abs(report[i] - report[j]);

    if ((diff > 3) || (diff == 0) || (!comp(report[i], report[j]))) {
      // we make two copies
      vector<int> without_i;
      vector<int> without_j;

      // resize them
      without_i.resize(report.size());
      without_j.resize(report.size());

      // copy them
      copy(report.begin(), report.end(), without_i.begin());
      copy(report.begin(), report.end(), without_j.begin());

      without_i.erase(without_i.begin() + i);
      without_j.erase(without_j.begin() + j);

      return (isValidReportV1(without_i, comp) ||
              isValidReportV1(without_j, comp));
    } else {
      i++;
      j++;
    }
  }
  return true;
}

s32 getValidReportCntV2(const std::vector<std::string>& lines) {
  using namespace std;
  vector<vector<s32>> reports = getReports(lines);

  s32 valid_reports_cnt{};
  for (const vector<int>& report : reports) {
    // logger->debug("Checking report: {}", report);
    if (isValidReportV2(report, std::greater<int>()) ||
        isValidReportV2(report, std::less<int>())) {
      // logger->debug("Report was valid!");
      valid_reports_cnt++;
    }
  }
  logger->debug("finished checking...");
  return valid_reports_cnt;
}

void day2_solve(const std::string& file_name, bool debug) {
  using namespace std;
  logger = getLogger("day2", debug);
  vector<string> lines = getLines(file_name);
  vector<vector<s32>> reports = getReports(lines);

  s32 valid_reports_part_1 = getValidReportCntV1(reports);
  logger->info("For part 1, there is {} valid reports", valid_reports_part_1);
  s32 valid_reports_part_2 = getValidReportCntV2(lines);
  logger->info("For part 2, there is {} valid reports.", valid_reports_part_2);
}
