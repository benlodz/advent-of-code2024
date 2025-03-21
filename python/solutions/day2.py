from typing import Callable
import argparse
import copy
from pathlib import Path
from .common import *

logger: logging.Logger
DAY: str = "day2"


def is_valid_report_v1(report: list[int], comparison: Callable) -> bool:
    """
    A report is valid if all numbers are either ascending or descending,
    and the difference between every value is at most 3 and at least 1.
    """
    i = 0
    j = 1
    N = len(report)

    # We can assume a report of 1 is valid.
    if N == 0 and N == 1:
        return True
    # A size of 2 will be valid as long as the difference is tolerable.
    # We now have an invariant that the report will have a length greater than 2.
    elif N == 2:
        difference = abs(report[i] - report[j])
        return 3 >= difference > 0

    while j < len(report):
        difference = abs(report[i] - report[j])

        if (not (3 >= difference > 0)) or (not comparison(report[i], report[j])):
            return False
        i += 1
        j += 1

    return True


def get_valid_report_cnt_v1(reports: list[list[int]]) -> int:

    cnt: int = 0
    for report in reports:
        if is_valid_report_v1(report, greater) or is_valid_report_v1(report, lesser):
            cnt += 1
    return cnt


def get_valid_report_cnt_v2(reports: list[list[int]]) -> int:

    cnt: int = 0
    for report in reports:
        if is_valid_report_v2(report, greater) or is_valid_report_v2(report, lesser):
            cnt += 1
    return cnt


def get_valid_report_cnt_v3(reports: list[list[int]]) -> int:
    cnt: int = 0
    for report in reports:
        if is_valid_report_v3(report, greater) or is_valid_report_v3(report, lesser):
            cnt += 1
    return cnt


def is_valid_report_v2(report: list[int], comparison: Callable):
    """
    In this scenario, we can tolerate one bad level.
    If a bad level is encountered.

    Example:
      i j
    1 3 2 4 5

    First we determine whether i can be adjacent to j + 1.
    If so, we can determine if it's valid if is_valid_report_v1
    works.

    Otherwise, we determine whether starting from j is valid.
    """
    i = 0
    j = 1

    N = len(report)

    # We can assume a report of 1 is valid.
    if N == 0 or N == 1:
        return True
    # A size of 2 will be valid as long as the difference is tolerable.
    # We now have an invariant that the report will have a length greater than 2.
    elif N == 2:
        difference = abs(report[i] - report[j])
        return 3 >= difference > 0

    while j < N:
        difference = abs(report[i] - report[j])

        if (not (3 >= difference > 0)) or (not comparison(report[i], report[j])):

            without_i = copy.deepcopy(report)
            without_i.pop(i)

            without_j = copy.deepcopy(report)
            without_j.pop(j)

            return is_valid_report_v1(without_i, comparison) or is_valid_report_v1(
                without_j, comparison
            )

        i += 1
        j += 1

    return True


def is_valid_report_v3(report: list[int], comparison: Callable):
    i = 0
    j = 1

    N = len(report)

    # We can assume a report of 1 is valid.
    if N == 0 or N == 1:
        return True
    # A size of 2 will be valid as long as the difference is tolerable.
    # We now have an invariant that the report will have a length greater than 2.
    elif N == 2:
        difference = abs(report[i] - report[j])
        return 3 >= difference > 0

    while j < N:
        difference = abs(report[i] - report[j])

        if (not (3 >= difference > 0)) or (not comparison(report[i], report[j])):

            # if we remove j, then everything up to i and j + 1 will be valid
            # we also have to verify i and j+1

            # we can tolerate the edge and j + 1 is guaranteed to be valid
            if (j + 1) == len(report):
                return True

            # check if we can remove j
            if (
                comparison(report[i], report[j + 1])
                and (3 > abs(report[i] - report[j + 1]) > 0)
                and is_valid_report_v1(report[j + 1 :], comparison)
            ):
                return True
            # if i == 0, we can just verify report[j:] is valid
            elif i == 0:
                return is_valid_report_v1(report[j:], comparison)
            # otherwise let's see if removing i we'll be valid
            elif (
                comparison(report[i - 1], report[j])
                and (3 > abs(report[i - 1] - report[j]) > 0)
                and is_valid_report_v1(report[j:], comparison)
            ):
                return True
            else:
                return False

        i += 1
        j += 1

    return True


def get_reports(lines: list[str]) -> list[list[int]]:
    """
    Lines come in the format of: "1, 2, 3, 4.."
    returns a list of these lines converted to a list of ints
    """
    return [[int(n) for n in line.split(" ")] for line in lines]


greater: Callable = lambda x, y: x > y
lesser: Callable = lambda x, y: x < y


def main():
    file_path: str
    file_path, logging_level = quick_parse(DAY)
    solve(Path(file_path), logging_level)


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    logger = get_logger(DAY, logging_level)

    lines: list[str] = read_file(file_path)
    reports: list[list[int]] = get_reports(lines)

    valid_reports_part_1: int = get_valid_report_cnt_v1(reports)
    logger.info(f"For part 1, the count of valid reports is: {valid_reports_part_1}.")

    valid_reports_part_2: int = get_valid_report_cnt_v3(reports)
    logger.info(f"For part 2, the count of valid reports is: {valid_reports_part_2}.")


if __name__ == "__main__":
    main()
