from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy


def get_towels(lines: List[str]) -> Tuple[List[str], List[str]]:
    """
    format:
    towels possibles

    target designs a
    target design b
    """
    global logger
    towels: List[str] = []
    target_designs: List[str] = lines[2:]

    # split by comma and then strip whitespace
    towels = [towel.strip() for towel in lines[0].split(",")]
    logger.debug(f"Found these towels:{towels}")

    logger.debug("Target Designs:")
    logger.debug(target_designs)

    return (towels, target_designs)


def get_designs_possible(lines: List[str]) -> Tuple[int, int]:

    towels: List[str]
    target_designs: List[str]
    List[str]
    towels, target_designs = get_towels(lines)
    target_designs_possible: int = 0

    designs_possible: int = 0

    DP: Dict = {}

    def backtrack(i: int, target: str, cur: str) -> int:

        # logger.debug("Entered backtrack function")
        # logger.debug(f"i:{i}\ttarget:{target}\tcur:{cur}")

        if (i, target) in DP:
            # logger.debug("Cache hit")
            return DP[(i, target)]

        if i >= len(target):
            # logger.debug("Bottomed out.")
            return 1

        # default value but I don't think it's needed
        res: int = 0
        for towel in towels:
            # logger.debug(f"Seeing if {towel} can work")

            # Does this towel align with target?
            # exit early if we find a successful possibility
            # logger.debug(f"Attempting to match it to {target[i: len(towel)]}")
            if towel == target[i : i + len(towel)] and (
                possible := backtrack(i + len(towel), target, cur + towel)
            ):
                res += possible
                continue

        DP[(i, target)] = res
        return DP[(i, target)]

    for target in target_designs:
        res = backtrack(0, target, "")
        if res:
            target_designs_possible += 1
        designs_possible += res

    return (target_designs_possible, designs_possible)


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    designs_possible: int
    design_possible_cnt: int
    designs_possible, design_possible_cnt = get_designs_possible(lines)
    logger.info(f"For Part 1, there is {designs_possible} designs possible.")
    logger.info(
        f"For Part 2, there is {design_possible_cnt} ways to make those designs."
    )


def main():
    file_path: str
    day: str = "day19"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
