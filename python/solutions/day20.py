from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy


def get_grid(lines: List[str]) -> List[List[str]]:

    grid: List[List[str]] = []

    for line in lines:
        grid.append([c for c in line])
    return grid


def get_cheat_cnt(lines: List[str]):

    grid: List[List[str]] = get_grid(lines)

    ROWS: int = len(grid)
    COLS: int = len(grid[0])

    start = None
    end = None
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "S":
                start = (r, c)
            if grid[r][c] == "E":
                end = (r, c)
            if start and end:
                break

    """
    Perform a BFS search
    At every step of the BFS, activate the cheat and take the difference 
    between how long it would take without the cheat
    """

    # baseline BFS
    q: Deque = deque()
    # pos, cost
    seen: Dict = {}
    # for typechecking
    r: int
    c: int
    nr: int
    nc: int

    def is_valid(r: int, c: int) -> bool:
        # (r, c) in bounds
        nonlocal ROWS
        nonlocal COLS
        return (r < ROWS) and (c < COLS) and (c >= 0) and (r >= 0)

    """
    We get the distance from the start on every single free tile.
    We are guaranteed there is one single path, so we don't need to worry
    about dead ends, we simply follow along the free spaces.
    """

    logger.debug("Beginning baseline BFS")
    r, c = start
    seen[(r, c)] = 0
    cost: int = 0
    while (r, c) != end:
        # logger.debug(f"Currently at {(r, c)}")
        for dr, dc in DIRECTIONS_4D:
            nr, nc = r + dr, c + dc
            # logger.debug(f"New position: {(nr, nc)}")
            if not is_valid(nr, nc):
                # logger.debug("invalid space!")
                continue
            elif grid[nr][nc] == "#":
                # logger.debug("encountered wall")
                continue
            elif (nr, nc) in seen:
                # logger.debug("Already visited this space")
                continue
            else:
                cost += 1
                seen[(nr, nc)] = cost
                r, c = nr, nc

    # cost is now baseline

    for k, v in seen.items():
        print(f"k:{k}, v:{v}")

    logger.debug(f"Baseline cost found: {cost}")

    res: int = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "#":
                continue
            for radius in range(2, 21):
                for dr in range(radius + 1):
                    dc = radius - dr
                    for nr, nc in {
                        ((r + dr), (c + dc)),
                        ((r - dr), (c + dc)),
                        ((r + dr), (c - dc)),
                        ((r - dr), (c - dc)),
                    }:
                        if not is_valid(nr, nc) or grid[nr][nc] == "#":
                            continue
                        if seen[(r, c)] - seen[(nr, nc)] >= 100 + radius:
                            res += 1

    return res


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    cheat_cnt: int = get_cheat_cnt(lines)
    logger.info(
        f"For part 1, there is {cheat_cnt} cheats that would allow you to save at least 100 picoseconds"
    )


def main():
    file_path: str
    day: str = "day20"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()

"""
40 doesn't work
41


1192130 too high for part 2


1143328 still too high
1142950 too high

1033643 was not right but getting closer...
"""
