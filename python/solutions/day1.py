from .common import *
from collections import Counter
from heapq import *
import copy
from pathlib import Path
import logging

logger: logging.Logger
DAY: str = "day1"


def get_similarity_score(lists: tuple[list, list]) -> int:
    l1: list[int]
    l2: list[int]

    l1, l2 = lists

    cnt: Counter = Counter(l2)
    similarity_score: int = 0

    for n in l1:
        if n in cnt:
            similarity_score += n * cnt[n]

    return similarity_score


def get_distance(lists: tuple[list, list]) -> int:

    h1: list[int] = copy.deepcopy(lists[0])
    h2: list[int] = copy.deepcopy(lists[1])

    heapify(h1)
    heapify(h2)

    distance: int = 0

    for _ in range(len(h1)):
        distance += abs(heappop(h1) - heappop(h2))

    return distance


def get_lists(lines: list[str]) -> tuple[list, list]:

    l1: list[int] = []
    l2: list[int] = []

    for line in lines:
        n1, n2 = line.split()
        l1.append(int(n1))
        l2.append(int(n2))

    return (l1, l2)


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    logger = get_logger(DAY, logging_level)
    lines: list[str] = read_file(file_path)

    lists: tuple[list, list] = get_lists(lines)

    distance: int = get_distance(lists)
    similarity_score: int = get_similarity_score(lists)

    logger.info(f"For part 1, the distance score is: {distance}.")
    logger.info(f"For part 2, the similarity score is: {similarity_score}.")


def main() -> None:
    file_path: str
    file_path, logging_level = quick_parse(DAY)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
