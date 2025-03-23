import re
from functools import reduce
from pathlib import Path
from .common import *

logger: logging.Logger
DAY: str = "day3"


def process_line(line: str) -> str:
    """
    If we encounter do() that means we can accept characters.
    Otherwise, once we get to don't(), we should reject characters,
    until we find another do().

    We assume that we're consuming characters at the beginning.
    """

    line_parts = []

    # these offsets are created based on the length of the do() and dont() command.
    dont_offset = 7
    do_offset = 4
    start = 0
    enabled = True
    for i, c in enumerate(line):
        # Adds everything up to the don't() call
        if c == "d" and enabled and line[i : i + dont_offset] == "don't()":
            line_parts.append(line[start:i])
            logger.debug(f"Adding {line_parts[-1]}")
            enabled = False
        # Renables from do()
        elif c == "d" and not enabled and line[i : i + do_offset] == "do()":
            enabled = True
            start = i

    # returns flattened string
    return "".join(line_parts)


def get_uncorrupted_mul(line: str) -> int:

    # uncorrupted mul instructions follow a certain pattern
    # that being mul({1,3},{1,3})
    # we use regex to match it and capture groups to isolate
    # the integers being multiplied.

    # this is only one big line
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
    total = 0

    # fancy one liner!
    return reduce(
        lambda x, y: x + y, map(lambda pair: int(pair[0]) * int(pair[1]), matches)
    )


def solve(file_path: Path, logging_level: int):
    global logger
    logger = get_logger(DAY, logging_level)
    lines: List[str] = read_file(file_path)
    line: str = "".join(lines)  # flatten file to one line

    # In this day, the puzzle input is one single line
    uncorrupted_mul_total: int = get_uncorrupted_mul(line)
    # we can reuse our function from part 1, we just need to transform the line
    enabled_mul_total: int = get_uncorrupted_mul(process_line(line))

    logger.info(
        f"For part 1, the total is with uncorrupted mul commands is: {uncorrupted_mul_total}."
    )
    logger.info(f"For part 2, the total for enabled mul is: {enabled_mul_total}.")


def main() -> None:
    file_path: str
    file_path, logging_level = quick_parse(DAY)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
