import argparse
import logging
import os

# The order of the tuples here represent a clockwise direction.
DIRECTIONS = (
    (-1, 0),  # going up
    (0, 1),  # going right
    (1, 0),  # going down
    (0, -1),  # going left
)


def get_args(desc: str, day: str):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help=desc,
        type=str,
    )
    parser.add_argument(
        "--debug", "-d", help="Turns on debugging statements.", action="store_true"
    )
    args = parser.parse_args()

    global logger
    logger = logging.getLogger(day)

    # Turn on debugging statements
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug("Debugging on!")

    return args.input if args.input else (day + "_sample.txt")


def get_input(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def get_distinct_positions_and_obstructions(lines: list[str]) -> int:
    """
    The runtime complexity will be near O(m * n) but not exactly.
    It's also the same case with memory since it's impossible to visit
    every single position in the grid.

    This is problem is trivial. We just keep a set of what positions
    we visited.
    """

    # First we need to find our starting position

    rows = len(lines)
    cols = len(lines[0])

    # This is making the assumption a guard will always be initially looking up.
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] == "^":
                start = (r, c)
                break

    def is_valid_pos(r: int, c: int) -> bool:
        if (r >= 0) and (r < rows) and (c >= 0) and (c < cols):
            return True
        else:
            return False

    r, c = start
    dir_idx: int = 0
    unique_positions: set = set()
    while is_valid_pos(r, c):
        unique_positions.add((r, c))

        # check for obstacles, if encountered rotate
        while True:
            r2, c2 = DIRECTIONS[dir_idx][0] + r, DIRECTIONS[dir_idx][1] + c
            if is_valid_pos(r2, c2) and lines[r2][c2] == "#":
                # if we hit an obstacle, we rotate
                dir_idx = (dir_idx + 1) % len(DIRECTIONS)
            else:
                break

        r, c = r2, c2

    def will_loop(start: tuple, obstruction: tuple) -> bool:
        """
        This will solve part 2 of the Day 6 question.
        That being, how many unique positions can we place an obstruction,
        in which the guard will be stuck in an infinite loop?

        While a bit naive, we can simply just place an obstruction for every unique
        position a guard will visit uninterrupted.

        We can determine whether he's stuck in a loop by seeing if he has
        visited both the same cell and is going the same direction.
        """

        seen = set()
        r, c = start
        dir_idx = 0
        while is_valid_pos(r, c):

            if (r, c, dir_idx) in seen:
                logger.debug(
                    f"Found a loop placing an obstruction at ({obstruction[0]},{obstruction[1]})"
                )
                return True

            seen.add((r, c, dir_idx))

            # rotate if we hit an obstacle
            while True:
                r2, c2 = DIRECTIONS[dir_idx][0] + r, DIRECTIONS[dir_idx][1] + c
                if is_valid_pos(r2, c2) and (
                    (lines[r2][c2] == "#") or ((r2, c2) == obstruction)
                ):
                    # if we hit an obstacle, we rotate
                    dir_idx = (dir_idx + 1) % len(DIRECTIONS)
                else:
                    break

            r, c = r2, c2
        return False

    will_loop_cnt = 0
    for pos in unique_positions:
        if will_loop(start, pos):
            will_loop_cnt += 1

    return (len(unique_positions), will_loop_cnt)


def main():
    file_path: str = get_args("Solution for Day 6 of the Advent of Code 2024", "day6")
    lines: list[str] = get_input(file_path)

    distinct_positions, obstruction_cnt = get_distinct_positions_and_obstructions(lines)

    print(f"The guard had a total of {distinct_positions} positions.")
    print(f"There are a total of {obstruction_cnt} positions to loop")


if __name__ == "__main__":
    main()
