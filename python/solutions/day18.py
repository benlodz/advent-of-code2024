from common import *
from typing import List, Tuple, Set, Dict, Deque
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy


def get_grid(lines: List[str], byte_cnt: int) -> List[List[str]]:
    global logger

    # grid is 0 to 70 both vertical & horizontally
    # so it's 71 x 71 grid
    N: int = 71

    # makes a 70 x 70 grid
    grid: List[List[str]] = [["." for _ in range(N)] for _ in range(N)]

    # simulate bytes
    for i in range(byte_cnt):
        line = lines[i]
        x, y = line.split(",")
        grid[int(x)][int(y)] = "#"

    return grid


def get_min_steps(lines: List[str], byte_cnt: int) -> int:
    global logger

    grid = get_grid(lines, byte_cnt)
    N: int = 71

    def is_valid(r: int, c: int) -> bool:
        return (r < N) and (c < N) and (r >= 0) and (c >= 0) and (grid[r][c] != "#")

    # Perform BFS
    q: Deque = deque()
    # pos, steps
    q.append(((0, 0), 0))
    seen: Set = set()

    while q:
        pos, steps = q.popleft()
        r, c = pos

        if pos in seen:
            continue
        else:
            seen.add(pos)

        if pos == (70, 70):
            return steps

        for dr, dc in DIRECTIONS_4D:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in seen:
                q.append(((nr, nc), steps + 1))

    logger.debug("Could not find valid path")
    return -1


def first_blocking_byte(lines: List[str]) -> int:

    for byte_cnt in range(1, len(lines)):
        logger.debug(f"Checking {byte_cnt}")
        steps_needed = get_min_steps(lines, byte_cnt)
        logger.debug(f"With {byte_cnt} bytes fallen, min step count: {steps_needed}")
        if steps_needed == -1:
            return lines[byte_cnt - 1]

    raise Exception("Didn't find a valid solution for first blocking byte")
    return -1


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    min_steps: int = get_min_steps(lines, 1024)
    logger.info(f"Min Steps: {min_steps}")

    min_byte_cnt: int = first_blocking_byte(lines)
    logger.info(f"byte cnt to block entrance: {min_byte_cnt}")


def main():
    file_path: str
    day: str = "day18"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
