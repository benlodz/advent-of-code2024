# from ..common.common import *
from math import floor
from collections import defaultdict
import argparse


def get_args(desc: str, day: str):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help=desc,
        type=str,
    )
    args = parser.parse_args()

    return args.input if args.input else (day + "_sample.txt")


def get_input(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def get_order_and_updates(lines: str) -> tuple:
    """
    the first section is in the format 11|22,
    so we can process that until we hit an empty line
    """

    ordering = defaultdict(set)
    i = 0
    while lines[i]:
        line = lines[i]
        # i don't have a better naming scheme yet
        # but pg2 is needed to print pg1
        pg1, pg2 = line.split("|")
        ordering[int(pg1)].add(int(pg2))
        i += 1
    i += 1

    updates = []
    while i < len(lines):
        updates.append([int(n) for n in lines[i].split(",")])
        i += 1
    print(ordering)
    return (ordering, updates)


def get_middle_total_v1(lines: list[str]) -> int:

    ordering, updates = get_order_and_updates(lines)

    def valid_update(update: list[int]) -> bool:
        print(f"Looking at this update {update}")
        # this is a n^2 operation
        # there might be a faster way to do this
        seen = set()
        for page in update:
            print(f"looking at this page: {page}")
            if page in ordering:
                reqs = ordering[page]
                print(f"These are the reqs: {reqs}")
                for req in reqs:
                    if req in seen:
                        return False
            seen.add(page)

        return True

    middle_total = 0
    for update in updates:
        if valid_update(update):
            print(f"This update is valid: {update}")
            middle_idx = floor(len(update) / 2)
            middle_total += update[middle_idx]

    return middle_total


def get_middle_total_with_corrections(lines: list[str]) -> int:

    ordering, updates = get_order_and_updates(lines)

    def correct_update(update: list[int]) -> None:
        """
        This will return a modified version of the update that
        respects the ordering rules.

        I think we can do this with a sorting algorithm but first
        I'm going to try it doing with an insert sort n^2
        """

        seen = set()

        for i in range(len(update)):
            pg = update[i]
            if pg in ordering:
                # Check if we've seen any pages that needs to be ahead
                move_back_index = -1
                # all the pages here are in correctly ahead of the current page.
                ahead_pages = ordering[pg] & seen
                smallest_index = float("inf")

                for j in range(i - 1, -1, -1):
                    if update[j] in ahead_pages:
                        smallest_index = min(smallest_index, j)
                if smallest_index != (float("inf")):
                    update.insert(smallest_index, pg)
                    # incorrect page is now displaced by one
                    update.pop(i + 1)

            seen.add(pg)

    def valid_update(update: list[int]) -> bool:
        print(f"Looking at this update {update}")
        # this is a n^2 operation
        # there might be a faster way to do this
        seen = set()
        for page in update:
            # print(f"looking at this page: {page}")
            if page in ordering:
                reqs = ordering[page]
                # print(f"These are the reqs: {reqs}")
                for req in reqs:
                    if req in seen:
                        return False
            seen.add(page)

        return True

    corrected_total = 0
    for update in updates:
        if not valid_update(update):
            print(f"This {update} was not valid")
            correct_update(update)
            print(f"Corrected: {update}")
            corrected_total += update[floor(len(update) / 2)]

    return corrected_total


def main():
    file_path = get_args("Solution for day 5.", "day5")
    lines = get_input(file_path)

    middle_total = get_middle_total_v1(lines)
    print(f"For all initial valid updates, the middle total is: {middle_total}.")

    corrected_middle_total = get_middle_total_with_corrections(lines)
    print(
        f"After correcting invalid updates, the middle total is: {corrected_middle_total}"
    )


main()

"""
5198 is too high
"""
