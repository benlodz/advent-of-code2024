import argparse
import logging
from array import array
from collections import defaultdict
import multiprocessing
from functools import cache

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


def get_arr(line: str) -> list[int]:
    return [int(c) for c in line.split()]


def get_digit_cnt(n: int) -> int:
    cnt: int = 0
    while n:
        cnt += 1
        n = n // 10
    return cnt


def get_split_n(n: int, cnt: int) -> tuple[int, int]:

    if cnt & 1:
        raise ValueError
    # this is kinda slow but works
    stack = []
    for _ in range(cnt // 2):
        stack.append(n % 10)
        n = n // 10

    left: int = n
    right: int = 0
    for digit in stack[::-1]:
        right *= 10
        right += digit

    return (left, right)


@cache
def get_arr_after_blink_v1(arr: list[int]):
    """
    To simulate our blinking we have to follow these rules:

    1. If the number is 0, change it to 1
    2. elif the stone has an even number of digits, it is split
    3. else the stone is multiplied by 2024
    """

    global blinks

    logger.debug(f"Initial array: {arr}")
    if type(arr) != list:
        raise ValueError("Test")

    for day in range(blinks):
        # iterate over the array applying the rules
        i = 0
        while i < len(arr):
            n: int = arr[i]
            digit_cnt: int = get_digit_cnt(n)
            logger.debug(f"Currently looking at {n}, digit cnt: {digit_cnt}")
            if not n:
                # equal to 0 rule
                arr[i] = 1
                i += 1
            elif not (digit_cnt & 1):
                # if even cnt
                left: int
                right: int
                left, right = get_split_n(n, digit_cnt)
                arr[i] = left
                arr.insert(i + 1, right)
                # increased offset by new value
                i += 2
            else:
                # multiply it by 2024
                arr[i] *= 2024
                i += 1
        logger.debug(f"day {day + 1} state of the array: {arr}")

    return arr


def get_arr_after_blink_v1_1(arr: list[int]):
    """
    this is a modified version for our mulitprocessing route in part 2
    """

    global blinks

    logger.debug(f"Initial array: {arr}")
    if type(arr) != list:
        raise ValueError("Test")

    # iterate over the array applying the rules
    i = 0
    while i < len(arr):
        n: int = arr[i]
        digit_cnt: int = get_digit_cnt(n)
        logger.debug(f"Currently looking at {n}, digit cnt: {digit_cnt}")
        if not n:
            # equal to 0 rule
            arr[i] = 1
            i += 1
        elif not (digit_cnt & 1):
            # if even cnt
            left: int
            right: int
            left, right = get_split_n(n, digit_cnt)
            arr[i] = left
            arr.insert(i + 1, right)
            # increased offset by new value
            i += 2
        else:
            # multiply it by 2024
            arr[i] *= 2024
            i += 1

    return arr


def chunkify(arr, n):
    return [arr[i::n] for i in range(n)]


def get_arr_after_blink_v2(arr: list[int]):
    cpu_cnt = multiprocessing.cpu_count()

    # for every day let's split our list into chunks

    for day in range(blinks):
        print(f"Working on day: {day}")
        # split our list into chunks
        chunks = chunkify(arr, cpu_cnt)
        # sanity check assert our chunking process
        for chunk in chunks:
            if type(chunk) != list:
                raise ValueError("This chunk isn't a list!")
        with multiprocessing.Pool(processes=cpu_cnt) as pool:
            result_chunks = pool.map(get_arr_after_blink_v1_1, chunks)

        # flatten our chunks into a single arr
        arr = [item for sublist in result_chunks for item in sublist]

    print(len(arr))


def get_arr_after_blink_v3(arr, blinks) -> int:

    @cache
    def dfs(stone: int, blinks: int) -> int:

        # base case
        if blinks == 0:
            return 1
        if stone == 0:
            return dfs(1, blinks - 1)

        digit_cnt = get_digit_cnt(stone)
        if not (digit_cnt & 1):
            left, right = get_split_n(stone, digit_cnt)
            return dfs(left, blinks - 1) + dfs(right, blinks - 1)
        else:
            return dfs(stone * 2024, blinks - 1)

    return sum([dfs(stone, blinks) for stone in arr])


def day11_solution():
    file_path = get_args("Solution for day 11", "day11")
    lines = get_input(file_path)

    arr: list[int] = get_arr(lines[0])
    print(arr)

    # stone_arr_part1: list[int] = get_arr_after_blink(lines[0], 75)
    # print(f"For part 1, there is {len(stone_arr_part1)} many stones.")
    print(get_arr_after_blink_v3(arr, 75))


if __name__ == "__main__":
    day11_solution()
