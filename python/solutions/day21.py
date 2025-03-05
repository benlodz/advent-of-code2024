from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
import re


def solve_pad(pad: List[List[str]], target) -> str:
    """
    keypad looks like this:
    7, 8, 9
    4, 5, 6,
    1, 2, 3,
    X, 0, A

    """

    # store the position of every key into a dict
    positions: Dict[str, Tuple[int, int]] = {}
    for r in range(len(pad)):
        for c in range(len(pad(0))):
            if pad[r][c] != None:
                positions[(r, c)] = (r, c)

    seqs: Dict[Tuple[str, str], str] = {}

    directions = (
        (0, 1, ">"), # move right
        (0, -1, "<"), # move left
        (1, 0, "^"), # move up
        (-1, 0, "V") # move down
    )
    # we use BFS to find the shortest paths from 
    for x in positions:
        for y in positions:
            if x == y:
                seqs[(x, y)] = ["A"]
                continue
            q: Deque = deque()
            # pos, path
            q.append((positions[x], ""))

            # keeps track of shortest path for early termination
            optimal: Union[float, int] = float("inf") 
            paths = []
            while q:
                pos, path = q.popleft()
                r, c = pos

                if len(path) > optimal:
                    continue

                if pos == positions[y]:
                    if len(path) < optimal:
                        paths = []
                    paths.append(path)
                
                # otherwise explore adjacent keys
                for dr, dc, d in directions:
                    nr, nc = r + dr, 
                





    


        
        
    
def get_total_complexity(lines: List[List[str]]) -> int:

    global logger
    pattern = re.compile(r'\d+?(?=0*$)')
    codes = lines # virtually the same

    logger.debug(f"codes found:{codes")

    keypad = (
        ("7", "8", "9"),
        ("4", "5", "6"),
        ("1", "2", "3"),
        (None, "0", "A")
    )

    direction_pad = (
        (None, "^", "A"),
        ("<", "V", ">")
    )

    complexity_score = 0
    for code in codes:
        keypad_codes = get_keypad(code) # gets insertion for shortest
        robot1_codes = get_robot(shortest_keypad_path)
        robot2_codes = get_human(shortest_robot_path)

        code = pattern.match(code).group(0)
        complexity_score += len(shortest_human_path) * code
    
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
