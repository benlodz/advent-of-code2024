from common import *
from typing import List, Tuple, Set, Dict, Deque
from pathlib import Path
from collections import deque, defaultdict
import heapq
import copy


def get_grid(lines: List[str]) -> List[List[str]]:
    grid: List[List[str]] = []
    for line in lines:
        grid.append([c for c in line])
    return grid


def pos_in_grid(grid: List[List[str]], pos: Tuple[int, int]) -> None:
    # For debugging purposes

    grid2 = copy.deepcopy(grid)
    ROWS = len(grid2)
    COLS = len(grid2[0])

    for r in range(ROWS):
        for c in range(COLS):
            if grid2[r][c] == "S":
                s_pos = (r, c)
                grid2[r][c] = "."
                grid2[pos[0]][pos[1]] = "S"

    for row in grid2:
        print("".join(row))


def get_smallest_score(grid: List[List[str]]) -> int:

    ROWS = len(grid)
    COLS = len(grid[0])

    """ 
    0 -> East
    1 -> South
    2 -> West
    3 -> North
    incrementing rotates clockwise and decrementing rotates counterclockwise
    """
    DIRECTIONS = ((0, 1), (-1, 0), (0, -1), (1, 0))

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "S":
                start = (r, c)

    # BFS search to find shortest path / smallest score
    q: Deque = deque()
    # pos, direction, current cost
    q.append((start, 0, 0))

    # pos, direction -> cost
    seen: Dict[tuple[int, int], int] = {}
    min_cost = float("inf")
    while q:
        pos, d, cost = q.popleft()
        r, c = pos

        if grid[r][c] == "E":
            min_cost = min(cost, min_cost)
            continue
        elif grid[r][c] == "#":
            # ### print("HIT WALL, EXIT!")
            continue

        # print(f"Currently at pos:{pos}, d:{DIRECTIONS[d]}, cost:{cost}")
        # print("*" * 10)
        # pos_in_grid(grid, pos)

        # if we've visited this cell with the same direction
        # and our cost is higher than before, return
        if (pos, d) in seen and cost > seen[(pos, d)]:
            continue
        else:
            seen[(pos, d)] = cost

        dr, dc = DIRECTIONS[d]  # explore in same direction
        q.append(((r + dr, c + dc), d, cost + 1))
        q.append(((r, c), ((d + 1) % 4), cost + 1000))
        q.append(((r, c), ((d - 1) % 4), cost + 1000))
        # print("-" * 10)
        # print("STATE of Q: ", q)
        # print("-" * 10)

    # print("This should never happen.")
    return min_cost


def get_tile_count(grid: List[List[str]]) -> int:

    ROWS = len(grid)
    COLS = len(grid[0])

    DIRECTIONS = ((0, 1), (-1, 0), (0, -1), (1, 0))

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "S":
                start = (r, c)

    # BFS search to find shortest path / smallest score
    pq = []
    # cost, pos, direction, visited
    pq.append((0, start, 0, []))

    # pos, direction -> cost
    seen: Dict[tuple[int, int], int] = {}
    min_cost = float("inf")
    best_tiles: List = []
    while pq:
        cost, pos, d, visited = heappop(pq)
        r, c = pos
        visited.append((pos))

        if cost > min_cost:
            continue

        if grid[r][c] == "E":
            # stupid hack
            if cost == 104516:
                best_tiles.extend(visited)

            continue
        elif grid[r][c] == "#":
            # ### print("HIT WALL, EXIT!")
            continue

        # print(f"Currently at pos:{pos}, d:{DIRECTIONS[d]}, cost:{cost}")
        # print("*" * 10)
        # pos_in_grid(grid, pos)

        # if we've visited this cell with the same direction
        # and our cost is higher than before, return
        if (pos, d) in seen and cost > seen[(pos, d)]:
            continue
        else:
            seen[(pos, d)] = cost

        dr, dc = DIRECTIONS[d]  # explore in same direction
        nr, nc = r + dr, c + dc
        if grid[nr][nc] != "#":
            heappush(pq, (cost + 1, (nr, nc), d, copy.deepcopy(visited)))
            # q.append(((nr, nc), d, cost + 1, copy.deepcopy(visited)))
        heappush(pq, ((cost + 1000), (r, c), ((d + 1) % 4), copy.deepcopy(visited)))
        heappush(pq, ((cost + 1000), (r, c), ((d - 1) % 4), copy.deepcopy(visited)))
        # q.append(((r, c), ((d + 1) % 4), cost + 1000, copy.deepcopy(visited)))
        # q.append(((r, c), ((d - 1) % 4), cost + 1000, copy.deepcopy(visited)))
        # print("-" * 10)
        # print("STATE of Q: ", q)
        # print("-" * 10)

    # print("This should never happen.")
    return len(set(best_tiles))


def get_score_tile_cnt(grid: List[List[str]]) -> Tuple[int, int]:

    ROWS = len(grid)
    COLS = len(grid[0])
    DIRECTIONS = ((0, 1), (-1, 0), (0, -1), (1, 0))

    pq: List = []
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "S":
                # cost, pos, direction,
                pq.append((0, (r, c), 0))

    # min cost we can achieve
    best_cost: int = float("inf")
    # cheapest cost to get to a cell
    lowest_cost: Dict = {}
    # parent cell from the cheapest path
    backtrack: Dict = {}
    # contains the cell and direction when we reach the goal
    end_states: Set = set()

    while pq:
        cost, pos, d = heapq.heappop(pq)
        r, c = pos
        dx, dy = DIRECTIONS[d]

        # skip cells we've seen with same or higher cost, otherwise float("inf")
        # let's us visit unseen cells
        # NOTE: second check maybe a clever hack but may not work
        if cost > lowest_cost.get((pos, d), float("inf")) or cost > best_cost:
            continue

        if grid[r][c] == "E":
            if cost > best_cost:
                continue
            best_cost = cost
            end_states.add((pos, d))

        lowest_cost[(pos, d)] = cost

        for new_cost, new_pos, new_d in (
            (cost + 1, (r + dx, c + dy), d),
            (
                cost + 1000,
                (r, c),
                ((d + 1) % 4),
            ),
            (
                cost + 1000,
                (r, c),
                ((d - 1) % 4),
            ),
        ):

            nr, nc = new_pos
            if grid[nr][nc] == "#":
                continue
            lowest = lowest_cost.get((new_pos, new_d), float("inf"))
            if new_cost > lowest:
                continue
            elif new_cost < lowest:
                lowest_cost[(new_pos, new_d)] = new_cost
                # new set since we found a cheaper path
                backtrack[(new_pos, new_d)] = set()
            backtrack[(new_pos, new_d)].add((pos, d))

            heapq.heappush(pq, (new_cost, new_pos, new_d))

    states = deque(end_states)
    seen = end_states

    while states:
        k = states.popleft()
        # get parent nodes / cells
        for last in backtrack.get(k, []):
            # ignore cells already explored
            if last in seen:
                continue
            seen.add(last)
            states.append(last)

    positions = [pos for pos, _ in seen]
    return (best_cost, len(set(positions)))


def solve(file_path: Path) -> None:
    lines: List[str] = read_file(file_path)
    grid: List[List[str]] = get_grid(lines)
    smallest_score_part1: int = get_smallest_score(grid)
    print("For part 1, the smallest possible score is: ", smallest_score_part1)

    # min_tiles = get_tile_count(grid)
    """
    print(
        "For part 2, for the shortest path the minimum amount of tiles seen: ",
        min_tiles,
    )
    """

    print("got: ", get_score_tile_cnt(grid))


def main():
    file_path: str = quick_parse("day16")
    solve(Path(file_path))


if __name__ == "__main__":
    main()
