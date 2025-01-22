import argparse
import logging
from array import array
from collections import defaultdict, deque
import multiprocessing
from functools import cache

# globals
logger: logging.Logger
# 0: right, 1: up, 2: down, 3: left
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


def get_total_costv1(lines: list[str]) -> int:
    """
    We should iterate over every cell and explore it's region.
    We can caculate the perimeter as we explore by checking
    adjacent cells. The area is just the amount in the region

    """

    seen: set = set()

    rows = len(lines)
    cols = len(lines[0])

    def is_valid(r: int, c: int) -> bool:
        # Checks if we're in bounds of our grid
        return (r >= 0) and (r < rows) and (c >= 0) and (c < cols)

    total_cost: int = 0

    q: deque = deque()

    def get_region_cost(r: int, c: int):

        area: int = 0
        perimeter: int = 0
        region = lines[r][c]
        q.append((r, c))

        while q:
            r, c = q.pop()

            if (r, c) in seen:
                continue

            seen.add((r, c))
            logger.debug(f"Currently at {(r, c)}")

            area += 1

            for d1, d2 in DIRECTIONS:
                r2: int = r + d1
                c2: int = c + d2
                if not is_valid(r2, c2) or lines[r2][c2] != region:
                    perimeter += 1
                else:
                    q.append((r2, c2))

        logger.debug(
            f"For {region}, starting at {(r, c)}, perimeter:{perimeter} and area: {area}. Total calculated: {perimeter * area}"
        )
        return perimeter * area

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in seen:
                total_cost += get_region_cost(r, c)

    return total_cost


def get_total_costv2(lines: list[str]) -> int:

    rows = len(lines)
    cols = len(lines[0])

    def is_valid(r: int, c: int) -> bool:
        # Checks if we're in bounds of our grid
        return (r >= 0) and (r < rows) and (c >= 0) and (c < cols)

    total_cost: int = 0
    seen: set = set()
    q: deque = deque()

    vertical_directions = ((1, 0), (-1, 0))
    horizontal_directions = ((0, 1), (0, -1))

    def get_region(r: int, c: int) -> None:
        region = lines[r][c]
        perimeter: set = set()
        area: int = 0
        q.append((r, c))

        while q:
            r1, c1 = q.popleft()

            if (r1, c1) in seen:
                continue

            seen.add((r1, c1))
            area += 1

            for dr, dc in DIRECTIONS:
                r2: int = r1 + dr
                c2: int = c1 + dc
                if is_valid(r2, c2) and lines[r2][c2] == region:
                    q.append((r2, c2))
                else:
                    perimeter.add((r1, c1, dr, dc))

        nonlocal total_cost
        sides: int = 0
        for r, c, dr, dc in perimeter:
            # if we have a change in the vertical direction / dr
            if dr != 0:
                # if we don't have a unit left of us
                if (r, c - 1, dr, dc) not in perimeter:
                    sides += 1
            # if we're moving laterally / horizontally / dc
            if dc != 0:
                if (r - 1, c, dr, dc) not in perimeter:
                    sides += 1

        logger.debug(
            f"Starting at {(r, c)}, region: {region}, area: {area}, sides: {sides}"
        )
        logger.debug(f"Perimeter contained these points: {perimeter}")
        total_cost += area * sides

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in seen:
                get_region(r, c)

    return total_cost


def solve_day12():
    file_path: str = get_args("Solution for day 12 of AoC 2024.", "day12")
    lines: list[str] = get_input(file_path)

    # total_cost_part1: int = get_total_costv1(lines)

    # print("For part 1, got this total cost for all regions: ", total_cost_part1)

    total_cost_part2: int = get_total_costv2(lines)
    print("For part 2, got this total cost for all regions: ", total_cost_part2)


if __name__ == "__main__":
    solve_day12()
