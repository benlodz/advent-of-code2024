#include <common/common.hpp>

template <typename Comparator>
bool isValidReportV1(const std::vector<s32> report, Comparator comp) {
  /*
  A report is valid if either it's ascending or descending,
  and the difference between two adjacent values fits the
  inequality of 1 <= diff <= 3
  */

  s32 diff{};
  for (int i{1}; i < report.length(); i++) {
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
    if (isValidReportV1(report, std::greater) ||
        isValidReportV1(report, std::lesser)) {
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

void solve_day2(const std::string& file_name) {
  using namespace std;
  vector<string> lines = getLines(file_name);
  vector<vector<s32>> reports = getReports(lines);

  s32 valid_reports_part_1 = getValidReportCntV1(reports);
}
