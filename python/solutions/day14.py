import argparse
import logging
from functools import reduce
import multiprocessing
import re
from math import ceil

# globals
logger: logging.Logger

# specifically for this problem
ROWS: int = 103
COLS: int = 101


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


def get_robots(lines: list[str]) -> list[tuple[int, ...]]:
    """
    Robots come in this format:
    p=0,4 v=3,-3
    The position being 0,4 and it's velocity is 3 right and 3 up
    """

    # .*? captures 0 or more characters in a non greedy way
    # so all the space between -? means optional negative sign
    # it's impossible for our pos to be negative, only slope
    pattern = re.compile(r"(\d+),(\d+).*?(-?\d+),(-?\d+)")

    robots = []
    for line in lines:
        if (matches := pattern.search(line)) is not None:
            robots.append(tuple(int(n) for n in matches.groups()))
        else:
            logger.debug(matches)
            logger.debug(f"got an empty line?, {line}")

    return robots


def get_robot_pos(robot, seconds) -> tuple[int, int]:
    # Returns the robots position after 100 seconds

    # unpack the robot
    x, y, dx, dy = robot

    return (((x + (dx * seconds)) % COLS), ((y + (dy * seconds)) % ROWS))


def get_robot_quadrant(robot_pos) -> int:
    """
    clockwise quadrants
    top right = 0
    bottom right = 1
    bottom left = 2
    top left = 3

    """
    x, y = robot_pos
    logger.debug(f"Getting robot at {x, y}'s quadrant")

    middle_row: int = ROWS // 2
    middle_col: int = COLS // 2

    if x == middle_col or y == middle_row:
        return -1

    # top right quadrant
    if x > (COLS // 2) and y < (ROWS // 2):
        return 0
    # bottom right
    elif x > (COLS // 2) and y > (ROWS // 2):
        return 1
    # bottom left
    elif x < (COLS // 2) and y > (ROWS // 2):
        return 2
    # otherwise must be top left
    else:
        return 3


def get_safety_factor(lines: list[str]) -> int:
    """
    First we need to get the positions of all the robots after 100 seconds,
    then we just need to determine it's quadrant and increment it

    """

    robots: list = get_robots(lines)

    quadrants: list[int] = [0, 0, 0, 0]

    # see if we can get a speedup with multiprocessing while waiting
    for robot in robots:

        robot_pos: tuple[int, int] = get_robot_pos(robot, 100)
        quadrant: int = get_robot_quadrant(robot_pos)
        logger.debug(f"Got this quadrant: {quadrant}")
        if quadrant != -1:
            quadrants[quadrant] += 1

    logger.debug(f"Final Quadrant State: {quadrants}")
    return reduce(lambda a, b: a * b, quadrants)


def has_christmas_tree(start, end, robots):
    robot_cnt = len(robots)
    for s in range(start, end):
        positions = set()
        for robot in robots:
            position = get_robot_pos(robot, s)
            if position not in positions:
                positions.add(position)
            else:
                continue
        if len(positions) == robot_cnt:
            return s
    print(f"Finished looking at ranges between {start} and {end}")
    return -1


def get_christmas_tree_mp(lines: list[str]):
    iterations = 100_000_00
    np = multiprocessing.cpu_count()

    chunk_size = iterations // np
    robots = get_robots(lines)

    with multiprocessing.Pool(processes=np) as pool:
        res = [
            pool.apply_async(
                has_christmas_tree, args=(i * chunk_size, (i + 1) * chunk_size, robots)
            )
            for i in range(np)
        ]

        if iterations % np != 0:
            res.append(
                pool.apply_async(
                    has_christmas_tree, args=(np * chunk_size, iterations, robots)
                )
            )

        for result in res:
            found_step = result.get()
            if found_step is not None:
                return found_step

    return -1


def get_christmas_tree(lines: list[str]):
    """
    There is a property that all robots will be in a unique
    position when there is a tree

    so whenever that happens, we have our answer

    """

    robots = get_robots(lines)
    robot_cnt = len(robots)
    # we'll do 10,000 iterations
    for s in range(100_000_000):
        # print("Currently looking at s: ", s)
        positions: set = set()
        for robot in robots:
            position = get_robot_pos(robot, s)
            if position in positions:
                continue
            else:
                positions.add(position)

        if len(positions) == robot_cnt:
            return s

    return -1


def solve_day14():
    file_path: str = get_args("Solution for day 14 AoC 2024", "day14")
    lines = get_input(file_path)

    safety_factor: int = get_safety_factor(lines)
    print(f"For part 1, the safety factor is: {safety_factor}")

    christmas_tree_s: int = get_christmas_tree_mp(lines)
    print(f"There is a christmas tree at {christmas_tree_s} seconds")


if __name__ == "__main__":
    solve_day14()


"""

224357412 correct!
"""
