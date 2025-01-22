import argparse
import logging
from array import array
from collections import defaultdict

# globals
logger: logging.Logger
rows: int
cols: int

DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))


def get_args(desc: str, day: str) -> str:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help=desc,
        type=str,
    )
    parser.add_argument(
        "--debug", "-d", help="Turns on debugging statements.", action="store_true"
    )
    args: argparse.Namespace = parser.parse_args()

    global logger
    logger = logging.getLogger(day)

    # Turn on debugging statements
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug("Debugging on!")

    return args.input if args.input else (day + "_sample.txt")


def get_input(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        lines: list[str] = f.read().splitlines()
        f.close()
    return lines


def get_grid(lines: list[list[str]]) -> list[list[int]]:
    """
    Returns the input as a 2D array of integers
    for conciseness.
    """

    grid: list[list[int]] = []

    for line in lines:
        grid.append([int(c) for c in line])

    return grid


def is_valid(r: int, c: int) -> bool:
    return (r >= 0) and (r < rows) and (c >= 0) and (c < cols)


def get_trailhead_sum(grid: list[list[int]]) -> int:
    """
    We iterate over the grid and everytime we find a 0, we calculate the amount of trails
    that can be created from it.

    """

    trailsum_cnt: int = 0

    global rows
    global cols
    rows = len(grid)
    cols = len(grid[0])

    seen_nine: set = set()

    def dfs(r: int, c: int) -> None:

        logger.debug(f"Currently at ({r},{c}), value: {grid[r][c]}")

        # base case
        if grid[r][c] == 9:
            logger.debug(f"Reached base case, storing {(r, c)} into seen nine set")
            seen_nine.add((r, c))

        for d1, d2 in DIRECTIONS:
            r2, c2 = r + d1, c + d2
            # if the next pos is valid and it's one step, explore
            if is_valid(r2, c2) and (grid[r2][c2] == (grid[r][c] + 1)):
                dfs(r2, c2)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                logger.debug(f"Looking at paths starting at: ({r},{c})")
                seen_nine.clear()
                dfs(r, c)
                trailsum_cnt += len(seen_nine)

    return trailsum_cnt


def get_trailhead_sum_v2(grid: list[list[int]]) -> int:
    """
    We iterate over the grid and everytime we find a 0, we calculate the amount of trails
    that can be created from it.

    """

    trailsum_cnt: int = 0

    global rows
    global cols

    DP: dict = {}

    def dfs(r: int, c: int) -> int:

        # cache
        if (r, c) in DP:
            return DP[(r, c)]

        logger.debug(f"Currently at ({r},{c}), value: {grid[r][c]}")

        # base case
        if grid[r][c] == 9:
            logger.debug(f"Reached base case!")
            return 1

        path_cnt: int = 0
        for d1, d2 in DIRECTIONS:
            r2, c2 = r + d1, c + d2
            # if the next pos is valid and it's one step, explore
            if is_valid(r2, c2) and (grid[r2][c2] == (grid[r][c] + 1)):
                path_cnt += dfs(r2, c2)

        DP[(r, c)] = path_cnt
        return DP[(r, c)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                logger.debug(f"Looking at paths starting at: ({r},{c})")
                trailsum_cnt += dfs(r, c)

    return trailsum_cnt


def day10_solution():
    file_path: str = get_args("Solution for day 10 of AoC 2024.", "day10")
    lines: list[list[str]] = get_input(file_path)

    grid: list[list[int]] = get_grid(lines)

    trailsum_cnt: int = get_trailhead_sum(grid)
    print(f"For part 1, the sum of all possible trailheads is: {trailsum_cnt}")

    trailsum_cnt_part2 = get_trailhead_sum_v2(grid)
    print(
        f"For part 2, the trailsum count with all possible paths is: {trailsum_cnt_part2}"
    )


if __name__ == "__main__":
    day10_solution()
