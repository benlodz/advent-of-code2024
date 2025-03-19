from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict, Union
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
from itertools import product, permutations, combinations
from dataclasses import dataclass
from functools import cache
import re
from math import floor

logger: logging.Logger


def get_matching_keys_and_locks(lines: List[str]) -> int:
    """
    locks and keys will always have the same dimensions.
    They seem to all be 7x5
    """
    global logger

    keys: List[List[List[str]]] = []
    locks: List[List[List[str]]] = []

    ROWS = 7
    COLS = 5

    i: int = 0
    while i < len(lines):
        temp = []
        while i < len(lines) and (line := lines[i]):
            temp.append([c for c in line])
            i += 1

        logger.debug("Printing out preallocation")
        for row in temp:
            logger.debug(row)

        # determine whether this is a key or a lock
        if temp[0][0] == "#":
            # lock
            logger.debug("Found lock!")
            locks.append(temp)
        else:
            # key
            logger.debug("Found key!")
            keys.append(temp)

        i += 1  # skip blank line

    def get_height(obj: List[List[str]], rev: bool = False):
        # if rev is false, it will determine height for a lock, going top -> down
        # otherwise it'll calculate heights bottom up

        heights: List[int] = []
        for c in range(COLS):
            height: int = -1  # offset since we're 0-indexed based
            if rev:
                for r in reversed(range(ROWS)):
                    if obj[r][c] == "#":
                        height += 1
                    else:
                        break
            else:
                for r in range(ROWS):
                    if obj[r][c] == "#":
                        height += 1
                    else:
                        break
            heights.append(height)

        return heights

    lock_heights: List[List[int]] = []
    for i, lock in enumerate(locks):
        lock_heights.append(get_height(lock))
        logger.debug(f"For lock {i}, we have a height of:{lock_heights[i]}")

    key_heights: List[List[int]] = []
    for i, key in enumerate(keys):
        key_heights.append(get_height(key, True))
        logger.debug(f"For key {i}, we have a height of:{key_heights[i]}")

    def can_fit(h1: List[int], h2: List[int]) -> bool:
        for x, y in zip(h1, h2):
            if (x + y) > 5:
                return False
        return True

    # assume we have k keys and l locks, this runs in O(k * l)
    matching: int = 0
    for k_height in key_heights:
        for l_height in lock_heights:
            if can_fit(k_height, l_height):
                matching += 1

    return matching


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    matching_key_and_locks = get_matching_keys_and_locks(lines)
    logger.info(
        f"For part 1, the amount of matching keys and locks are:{matching_key_and_locks}"
    )


def main():
    file_path: str
    day: str = "day25"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
