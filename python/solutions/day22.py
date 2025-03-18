from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict, Union
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
from itertools import product
from functools import cache
import re
from math import floor


def get_secret_numbers(lines: List[str]) -> List[int]:
    return [int(line) for line in lines]


def mix_and_prune(a: int, b: int) -> int:
    a ^= b
    return a % 16777216


def get_secret_number_sum(secret_numbers: List[int], cnt: int) -> int:

    secret_number_sum: int = 0
    for secret_number in secret_numbers:
        for _ in range(cnt):
            # first step
            secret_number = mix_and_prune(secret_number, secret_number * 64)
            # second step
            secret_number = mix_and_prune(secret_number, floor(secret_number / 32))
            # third step
            secret_number = mix_and_prune(secret_number, secret_number * 2048)
        secret_number_sum += secret_number
    return secret_number_sum


def get_max_bananas(secret_numbers: List[int], cnt: int) -> int:

    # idx of secret number represents list of prices for 2000 days
    seller_to_secret_numbers: DefaultDict[int, List[int]] = defaultdict(list)

    for i, secret_number in enumerate(secret_numbers):
        for _ in range(cnt):

            seller_to_secret_numbers[i].append(secret_number)

            # first step
            secret_number = mix_and_prune(secret_number, secret_number * 64)
            # second step
            secret_number = mix_and_prune(secret_number, floor(secret_number / 32))
            # third step
            secret_number = mix_and_prune(secret_number, secret_number * 2048)

    # Create dictionary for a given seller, will create a list
    # that holds the actual selling price for that given second
    seller_to_bananas: DefaultDict[int, List] = defaultdict(list)
    for seller in range(len(secret_numbers)):
        seller_numbers = seller_to_secret_numbers[seller]
        for seller_number in seller_numbers:
            seller_to_bananas[seller].append(seller_number % 10)

    # Create a separate list that holds the changes at every given second
    seller_to_changes: DefaultDict[int, List] = defaultdict(list)
    for seller in range(len(secret_numbers)):
        prices = seller_to_bananas[seller]
        seller_to_changes[seller].append(
            None
        )  # the first value has no change so consider this NIL
        prev = prices[0]
        i = 1
        while i < len(prices):
            seller_to_changes[seller].append(prices[i] - prev)
            prev = prices[i]
            i += 1

    """
    we want to get every possible sequence
    we also want to quickly see whether that sequence exist for a seller and what that would result
    we can than iterate over seqs and take the max of it
    """

    # given a seller and a seqs, returns the price that seqs would give
    seller_and_seqs_to_price: Dict[int, Tuple[int, int, int, int]] = {}
    seqs: Set = set()  # all possible seqs
    for seller in range(len(secret_numbers)):
        # window, we skip 0 because it's None
        window: Deque[int] = deque()
        changes = seller_to_changes[seller]
        for i, n in enumerate(changes[1:]):
            window.append(n)
            if len(window) == 4:
                seq = tuple(window)
                logger.debug(f"found this seq: {seq} for this seller:{seller}")
                seqs.add(seq)
                if (seller, seq) not in seller_and_seqs_to_price:
                    logger.debug(
                        f"Adding {seller_to_bananas[seller][i + 1]} for {(seller, seq)}"
                    )
                    seller_and_seqs_to_price[(seller, seq)] = seller_to_bananas[seller][
                        i + 1
                    ]
                window.popleft()

    most_bananas = 0
    for seq in seqs:
        logger.debug(f"looking at this sequence: {seq}")
        bananas = 0
        for seller in range(len(secret_numbers)):
            if (seller, seq) in seller_and_seqs_to_price:
                bananas += seller_and_seqs_to_price[(seller, seq)]
        logger.debug(f"Bananas found for this seq: {bananas}")
        most_bananas = max(bananas, most_bananas)

    return most_bananas


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    secret_numbers = get_secret_numbers(lines)
    secret_numbers_sum = get_secret_number_sum(secret_numbers, 2000)
    print("ran")
    logger.info(
        f"For part 1, the sum of secret numbers up to day 2000 is: {secret_numbers_sum}"
    )
    print(get_max_bananas(secret_numbers, 2000))


def main():
    file_path: str
    day: str = "day22"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
