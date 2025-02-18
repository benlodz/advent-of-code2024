from common import *
from typing import List, Tuple, Set, Dict
from pathlib import Path
import copy


def parse_file(file: List[str]) -> Tuple[List[List[str]], List[str]]:

    grid: List[List[str]] = []
    i: int = 0
    while file[i]:
        grid.append(list(file[i]))
        i += 1

    # i will stop on the blank line
    moves: List[str] = []

    for j in range(i + 1, len(file)):
        moves.extend(file[j])
    return (grid, moves)


def simulate_robot(grid: List[List[str]], moves: List[str]) -> List[List[str]]:

    ROWS = len(grid)
    COLS = len(grid[0])

    # find the starting position of the robot
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "@":
                current = [r, c]

    # Map arrows to direction
    directions = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    for move in moves:
        r, c = current
        dx, dy = directions[move]
        nr, nc = r + dx, c + dy

        if grid[nr][nc] == ".":
            grid[r][c] = "."
            grid[nr][nc] = "@"
            current = [nr, nc]
        elif grid[nr][nc] == "O":
            # ("Found box")

            # look up ahead until we find either a . or #
            while grid[nr][nc] == "O":
                nr += dx
                nc += dy

            # (f"ended at {(nr, nc)}, contains {grid[nr][nc]}")
            if grid[nr][nc] == ".":
                # (f"Found free space at {(nr, nc)}")
                while grid[nr][nc] != "@":
                    grid[nr][nc] = "O"
                    nr -= dx
                    nc -= dy

                # final shift
                grid[r + dx][c + dy] = "@"
                grid[r][c] = "."
                current = [r + dx, c + dy]

        # (f"Current state of the grid, move attempted: {move}")
    return grid


def get_gps_sum(grid: List[List[str]]) -> int:
    ROWS = len(grid)
    COLS = len(grid[0])

    gps_score: int = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "O":
                gps_score += (100 * r) + c

    return gps_score


def get_gps_sum_v2(grid: List[List[str]]) -> int:
    ROWS = len(grid)
    COLS = len(grid[0])

    gps_score: int = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "[":
                gps_score += (100 * r) + c

    return gps_score


def get_wide_grid(grid: List[List[str]]) -> List[List[str]]:
    """
    # -> ##
    O -> []
    . -> ..
    @ -> @.
    """

    ROWS = len(grid)
    COLS = len(grid[0])

    second_layers: List[List[str]] = []

    for r in range(ROWS):
        layer = []
        for c in range(COLS):
            char = grid[r][c]
            if char == ".":
                layer.append(".")
            elif char == "O":
                grid[r][c] = "["
                layer.append("]")
            elif char == "#":
                layer.append("#")
            elif char == "@":
                layer.append(".")
        second_layers.append(layer)

    # merge the grids
    wide_grid: List[List[str]] = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(grid[r][c])
            row.append(second_layers[r][c])
        wide_grid.append(row)

    return wide_grid


def simulate_wide_robot(grid: List[List[str]], moves: List[str]) -> List[List[str]]:

    ROWS = len(grid)
    COLS = len(grid[0])

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "@":
                pos = [r, c]

    # Map arrows to direction
    directions = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    can_push_all: bool = False
    visit: Set = set()
    new_pos: Dict = {}

    ("Initial Grid:")
    for row in grid:
        ("".join(row))

    def can_push(pos: Tuple[int, int], move: Tuple[int, int]) -> None:
        """
        This is the recursive call to check whether we can the box
        pos is the position
        move is the direction we're moving in
        we don't want infinite recursion when checking sides

        """

        r, c = pos
        # (f"function: can_push, current pos:{(r, c)}")
        dx, dy = move
        nr, nc = r + dx, c + dy
        char = grid[r][c]

        # to update
        nonlocal can_push_all

        if (r, c) in visit:
            # ("early exit!")
            return
        else:
            visit.add((r, c))

        if grid[r][c] == "#":
            can_push_all &= False
            return

        elif grid[r][c] == ".":
            can_push_all &= True
            return

        new_pos[(nr, nc)] = char
        # look ahead if we can push it in direction of move
        can_push((nr, nc), move)

        # prevent infinite recursion when checking if side is valid too
        if char == "[":
            can_push((r, c + 1), move)
        else:
            can_push((r, c - 1), move)

    for move in moves:
        r, c = pos
        dx, dy = directions[move]
        nr, nc = r + dx, c + dy
        char = grid[nr][nc]

        if char == ".":
            grid[r][c] = "."
            grid[nr][nc] = "@"
            pos = [nr, nc]
        elif (char == "[") or (char == "]"):

            (f"checking if we can push box at {(nr, nc)}")
            (f"@ is currently at pos:{(r, c)}")

            ("state of current grid:")
            for row in grid:
                ("".join(row))
            # setup
            can_push_all = True
            visit.clear()
            new_pos.clear()

            can_push((nr, nc), (dx, dy))

            if can_push_all:
                ("new positions: ", new_pos.items())
                for box_pos, box_char in new_pos.items():
                    br, bc = box_pos
                    grid[br][bc] = box_char

                for box_pos in visit:
                    if box_pos not in new_pos:
                        er, ec = box_pos
                        grid[er][ec] = "."

                grid[nr][nc] = "@"
                grid[r][c] = "."
                pos = [nr, nc]

            ("Printing grid after push")
            for row in grid:
                ("".join(row))

        elif char == "#":
            pass

    return grid


def get_gps_score_v1(grid: List[List[str]], moves: List[str]) -> int:

    working_grid = copy.deepcopy(grid)
    final_grid: List[List[str]] = simulate_robot(working_grid, moves)

    return get_gps_sum(final_grid)


def get_gps_score_v2(grid: List[List[str]], moves: List[str]) -> int:

    working_grid: List[List[str]] = copy.deepcopy(grid)
    wide_grid: List[List[str]] = get_wide_grid(working_grid)

    final_grid: List[List[str]] = simulate_wide_robot(wide_grid, moves)

    for row in final_grid:
        ("".join(row))

    return get_gps_sum_v2(final_grid)
    return 0


def solve(file_path: Path) -> None:
    lines: List[str] = read_file(file_path)
    grid: List[List[str]]
    moves: List[str]

    grid, moves = parse_file(lines)

    gps_score_part1: int = get_gps_score_v1(grid, moves)
    ("For part 1, the calculated GPS score was: ", gps_score_part1)

    gps_score_part2: int = get_gps_score_v2(grid, moves)
    ("For part 2, the calculated GPS score was: ", gps_score_part2)


def main():
    file_path: str = quick_parse("day15")
    solve(Path(file_path))


if __name__ == "__main__":
    main()
