import argparse
import logging
import re
from array import array
from collections import defaultdict, deque
import multiprocessing
from functools import cache
from z3 import *

# globals
logger: logging.Logger


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


def get_machines(
    lines: list[str],
) -> list[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """
    The input comes in the form of:
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    empty line
    """

    machines = []
    for i in range(0, len(lines), 4):
        # \d to match digit, .*? captures character inbetween non-greedy
        pattern = re.compile(r"(\d+).*?(\d+)")
        # get the A button
        matches = pattern.search(lines[i])
        A: tuple[int, int] = (int(matches.group(1)), int(matches.group(2)))
        # get the B button
        matches = pattern.search(lines[i + 1])
        B: tuple[int, int] = (int(matches.group(1)), int(matches.group(2)))
        # get the amount needed for the prizes
        matches = pattern.search(lines[i + 2])
        PRIZES: tuple[int, int] = (int(matches.group(1)), int(matches.group(2)))

        logger.debug(f"Found this machine\n A:{A}\nB:{B}\nPRIZES:{PRIZES}")
        machines.append((A, B, PRIZES))

    return machines


def get_min_cost(machine) -> int:
    """
    I'm pretty sure we can solve this with DP
    It's also worth noting it may be impossible to solve a given machine
    A Button is 3 tokens
    B button is 1 token

    """

    # unpack the tuple
    A, B, PRIZES = machine

    A_X, A_Y = A
    B_X, B_Y = B
    TARGET_X, TARGET_Y = PRIZES

    DP: dict = {}

    def dfs(pos: tuple, cost: int) -> int | float:

        if pos in DP:
            return DP[pos]

        x, y = pos
        # if we go pass our target
        if x > TARGET_X or y > TARGET_Y:
            return float("inf")

        # base case if we hit our target
        if x == TARGET_X and y == TARGET_Y:
            return cost

        # hit the A button
        a_cost = dfs((x + A_X, y + A_Y), cost + 3)

        # hit the B button
        b_cost = dfs((x + B_X, y + B_Y), cost + 1)

        min_cost = min(a_cost, b_cost)
        DP[pos] = min_cost
        return DP[pos]

    min_cost = dfs((0, 0), 0)
    if min_cost == float("inf"):
        return 0
    else:
        return min_cost


def get_prize_cnt_v1(lines: list[str]) -> int:
    """ """

    machines: list[tuple[int, int, int]] = get_machines(lines)

    machine_cost: list[int] = [get_min_cost(machine) for machine in machines]

    return sum(machine_cost)


def get_prize_cnt_v2(lines: list[str]) -> int:
    machines = get_machines(lines)

    min_coins: int = 0
    for machine in machines:

        # unpack machine
        A, B, PRIZES = machine

        A_X, A_Y = A
        B_X, B_Y = B
        TARGET_X, TARGET_Y = PRIZES

        TARGET_X += 10000000000000
        TARGET_Y += 10000000000000

        s = Solver()

        a = Int("a")
        b = Int("b")

        s.add(a >= 0)
        s.add(b >= 0)

        s.add((a * A_X) + (b * B_X) == TARGET_X, (a * A_Y) + (b * B_Y) == TARGET_Y)
        if s.check() == sat:
            model = s.model()

            a_val = model.eval(a).as_long()
            b_val = model.eval(b).as_long()

            min_coins += b_val + (3 * a_val)

    return min_coins


def get_prize_cnt_v3(lines: list[str]) -> int:

    machines = get_machines(lines)

    min_cost: int = 0
    for machine in machines:
        A, B, PRIZES = machine

        ax, ay = A
        bx, by = B
        tx, ty = PRIZES

        tx += 10000000000000
        ty += 10000000000000

        a = ((tx * by) - (bx * ty)) // ((ax * by) - (ay * bx))
        b = (ty - (a * ay)) // by

        if (((a * ax) + (b * bx)) == tx) and (((a * ay) + (b * by)) == ty):
            min_cost += b + (a * 3)

    return min_cost


def solve_day13():
    file_path: str = get_args("Solution for day13 of AoC 2024.", "day13")
    lines: list[str] = get_input(file_path)

    min_cost_for_all_prizes: int = get_prize_cnt_v1(lines)
    print(f"The most amount of prizes you can get is: ", min_cost_for_all_prizes)

    min_coins_part2: int = get_prize_cnt_v2(lines)
    print(f"For part 2, min coins we can spend is: ", min_coins_part2)

    print(get_prize_cnt_v3(lines))


if __name__ == "__main__":
    solve_day13()


"""
875318608908 too low??

"""
