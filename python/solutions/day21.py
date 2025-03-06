from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict, Union
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
from itertools import product
import re


def solve_pad(pad: Tuple[Tuple[str]], target: str) -> str:
    """
    keypad looks like this:
    7, 8, 9
    4, 5, 6,
    1, 2, 3,
    X, 0, A

    """

    # store the position of every key into a dict
    positions: Dict[str, Tuple[int, int]] = {}

    ROWS: int = len(pad)
    COLS: int = len(pad[0])

    for r in range(ROWS):
        for c in range(COLS):
            if pad[r][c] != None:
                positions[pad[r][c]] = (r, c)

    seqs: Dict[Tuple[str, str], List[str]] = {}

    directions = (
        (0, 1, ">"),  # move right
        (0, -1, "<"),  # move left
        (1, 0, "V"),  # move up
        (-1, 0, "^"),  # move down
    )
    # we use BFS to find the shortest paths
    # from one key to another
    for x in positions:
        for y in positions:
            if x == y:
                seqs[(x, y)] = ["A"]
                continue

            # logger.debug(f"Looking for optimal paths from {x} to {y}")
            q: Deque = deque()
            # pos, path
            q.append((positions[x], ""))

            # keeps track of shortest path for early termination
            optimal: Union[float, int] = float("inf")
            paths: List[str] = []

            while q:
                pos, path = q.popleft()
                r, c = pos

                # early exit if path is longer than optimal
                if len(path) > optimal or (
                    len(path) == optimal and pos != positions[y]
                ):
                    continue

                if pos == positions[y]:
                    if (len(path) + 1) < optimal:
                        paths = []
                        optimal = len(path) + 1
                    paths.append(path + "A")
                    continue

                # otherwise explore adjacent keys
                for dr, dc, d in directions:
                    nr, nc = r + dr, c + dc
                    if (
                        (nr >= 0)
                        and (nr < ROWS)
                        and (nc >= 0)
                        and (nc < COLS)
                        and pad[nr][nc] is not None
                    ):
                        q.append(((nr, nc), path + d))
            seqs[(x, y)] = paths

    # logger.debug(seqs)
    # now we find to make all possible shortest insertions
    # options = [seqs[(x, y)] for x, y in zip("A" + target, target)]
    options = []
    for x, y in zip("A" + target, target):
        options.append(seqs[(x, y)])
    logger.debug(options)
    possible_seqs = ["".join(x) for x in product(*options)]
    print(possible_seqs)
    return ""


def get_total_complexity(lines: List[List[str]]) -> int:

    global logger
    pattern = re.compile(r"\d+?(?=0*$)")
    codes = lines  # virtually the same

    logger.debug(f"codes found:{codes}")

    keypad = (("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), (None, "0", "A"))

    direction_pad = ((None, "^", "A"), ("<", "V", ">"))

    complexity_score = 0
    for code in codes:
        keypad_codes = solve_pad(keypad, code)  # gets insertion for shortest
        """
        robot1_codes = get_robot(shortest_keypad_path)
        robot2_codes = get_human(shortest_robot_path)

        code = pattern.match(code).group(0)
        complexity_score += len(shortest_human_path) * code
        """

    return complexity_score


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    get_total_complexity(lines)


def main():
    file_path: str
    day: str = "day21"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()

"""
There is a keypad that a robot is trying to press

1. figure out the shortest sequence for keypad
2. figure out shortest sequence to enter for keypad
3. figure out the shortest sequence for my keypad
4. do this for the input
5. calculate complexity and sum it up


"""
