import argparse
import logging
from array import array
from collections import defaultdict

# globals
logger: logging.Logger
rows: int
cols: int


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


def get_checksum(lines: list[str]) -> int:

    line: str = lines[0]

    # These pointers are used in our input string
    # the left pointer is placed at block size, the next indice is free space
    # the right pointer will always move by 2 since we're only interested in
    # consuming block from it.
    l, r = 0, len(line) - 1
    checksum: int = 0

    # Our string represents pairs (block size, free space)
    # so naturally, dividing by 2 should give us the amount of units here
    # However, we do integer division to floor it since the last value
    # does not have free space
    right_id = len(line) // 2
    left_id: int = 0

    # we're making the assumption here that the last
    # block doesn't have any free spaces ahead of it
    right_block_cnt = int(line[r])

    # this represents how many times we added to our compact string
    checksum_idx: int = 0

    while (l < len(line)) and (l < r):

        logger.debug(
            f"""
        Currently at indice: {l}, val: {line[l]},
        left id: {left_id}, right id: {right_id},
        current checksum: {checksum}
        right ptr: {r}
        """
        )

        # First we add to the checksum per block
        for _ in range(int(line[l])):
            logger.debug(f"Adding {(left_id * checksum_idx)} to checksum")
            checksum += left_id * checksum_idx
            checksum_idx += 1

        # get free blocks
        free_blocks = int(line[l + 1])
        logger.debug(f"Free blocks: {free_blocks}")

        # if we have free space
        while free_blocks:
            logger.debug(f"Current blocks on right side: {right_block_cnt}")
            # we still have blocks to consume from the right side
            while free_blocks and right_block_cnt:
                logger.debug(f"Adding {(right_id * checksum_idx)} to checksum")
                checksum += right_id * checksum_idx
                right_block_cnt -= 1
                checksum_idx += 1
                free_blocks -= 1

            if not free_blocks:
                logger.debug("Ran out of free blocks to use!")
                break
            # if we run out move to the next character
            # we're only interested in the amount of space consumed, not free space
            r -= 2
            right_id -= 1
            right_block_cnt = int(line[r])

            if l == r:
                # if our pointers overlap, just return
                logger.debug("Early return, ran out of space on right side!")
                return checksum

        # move onto next block
        l += 2
        left_id += 1

    while right_block_cnt:
        checksum += right_id * checksum_idx
        checksum_idx += 1
        right_block_cnt -= 1
    return checksum


def get_checksum_v2(line: str):
    """
    Compared to other solutions online, this is relatively slow
    and significantly more complicated.

    First I preprocess the array, given a block like this 23
    where we have a block of length 2 and 3 free blocks ahead,
    I would put it's ID in front to something like this: 023
    ID = 0, block space = 2, and free space = 3

    After making this new array, it does a linear scan for the highest id.
    Then another linear scan for the leftmost space for a possible insertion.

    I ran into a bug that took a while to solve, here is the tl;dr
    00... -> 99, in this scenario it would become 0099.
    I would store the initial free space 3 and then subtract the block size 2,
    normally after insertions and deletions, you'd get something like this 020921
    ID 0, block size 2, 0 free space, ID 9, 2 blocks, and finally 1 free space.

    After doing that transformation, the block with ID 8 would gain it's block size
    and free space.

    However in this edge case, 666...777
    I would store the initial free space and then subtract it by the block size.
    However, it should gain the space right of 777 and then calculate the wrong answer.
    """

    pre = []
    i = 0
    current_id: int = 0
    while i < len(line) - 1:
        # insert the id
        pre.append(current_id)
        # insert the amount of blocks taken
        pre.append(int(line[i]))
        # insert free space
        pre.append(int(line[i + 1]))
        i += 2
        current_id += 1

    pre.append(current_id)
    pre.append(int(line[i]))
    pre.append(0)

    # the r pointer is placed at the block size
    # r + 1 is free space
    # r - 1 is it's ID
    right_id = current_id

    # can left ID's be moved once too?
    while right_id > 0:
        # find the right id
        i = 0
        while i < len(pre):
            if pre[i] == right_id:
                r = i + 1
                break
            i += 3
        right_block_size: int = pre[r]

        right_free_space: int = pre[r + 1]

        # scan the left side for an insertion point
        l = 2
        while l < r:
            left_free_space = pre[l]

            # we can insert here
            if left_free_space >= right_block_size:

                print(f"This is the space before right id: {pre[r - 2]}")

                # set the next left block from right to have right's space
                pre[r - 2] += right_free_space + right_block_size
                new_free_space = pre[l] - right_block_size
                del pre[r - 1]
                del pre[r - 1]
                del pre[r - 1]

                # there is no more free space for this file because we consumed it
                pre[l] = 0
                # insert the ID
                pre.insert(l + 1, right_id)
                # insert the block size
                pre.insert(l + 2, right_block_size)
                # insert the new free space

                pre.insert(l + 3, new_free_space)

                break
            else:
                l += 3
        right_id -= 1

    checksum = 0
    checksum_idx = 0
    i = 0

    while i < len(pre):
        block_id = pre[i]
        block_size = pre[i + 1]

        for _ in range(block_size):
            checksum += block_id * checksum_idx
            checksum_idx += 1

        # move our index by empty blocks
        checksum_idx += pre[i + 2]
        i += 3
    return checksum


def day9_solution():
    file_path = get_args("Solution for Day 9", "day9")
    lines = get_input(file_path)

    part1_checksum: int = get_checksum(lines)

    part2_checksum: int = get_checksum_v2(lines[0])

    print(f"The checksum for part 1: {part1_checksum}")
    print(f"The checksum for part 2: {part2_checksum}")


if __name__ == "__main__":
    day9_solution()
