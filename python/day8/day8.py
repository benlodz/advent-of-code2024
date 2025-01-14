import argparse
import logging
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


def valid_pos(pos: tuple[int, int]) -> bool:
    r: int
    c: int
    r, c = pos
    global rows
    global cols

    return not ((r >= rows) or (r < 0) or (c < 0) or (c >= cols))


def print_node(node: tuple[int, int]) -> str:
    return f"({node[0]},{node[1]})"


def get_symbols(lines: list[list[str]]) -> defaultdict:

    global rows
    global cols

    rows = len(lines)
    cols = len(lines[0])
    symbols = defaultdict(list)

    # First let's iterate over all lines and collect all possible antennas
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] != ".":
                symbols[lines[r][c]].append((r, c))

    if logger.getEffectiveLevel() == logging.DEBUG:
        for k, v in symbols.items():
            logger.debug(f"Symbol: {k}, found at these locations: {v}")

    return symbols


def get_antinodes_v1(node_a: tuple[int, int], node_b: tuple[int, int]):
    """
    Part 1 Intuition:
    Antinodes are located twice the distance away from two cells.
    As long as they share the same symbol.

    So first we calculate the difference between the two nodes.
    We can then use this distance to calculate the location of the
    anti node.

    Example:
    (5,6) & (8, 8)
    5 - 8 = -3
    6 - 8 = -2

    The antinode twice the distance from (8,8) will be
    (5 + (-3), 6 + (-2)) = (2, 4)
    """

    anti_nodes = []

    node_a_anti_node_offset = (node_a[0] - node_b[0], node_a[1] - node_b[1])
    node_b_anti_node_offset = (node_b[0] - node_a[0], node_b[1] - node_a[1])

    node_a_anti_node = (
        node_a[0] + node_a_anti_node_offset[0],
        node_a[1] + node_a_anti_node_offset[1],
    )
    node_b_anti_node = (
        node_b[0] + node_b_anti_node_offset[0],
        node_b[1] + node_b_anti_node_offset[1],
    )

    if valid_pos(node_a_anti_node):
        anti_nodes.append(node_a_anti_node)

    if valid_pos(node_b_anti_node):
        anti_nodes.append(node_b_anti_node)

    if logger.getEffectiveLevel() == logging.DEBUG:
        logger.debug("Found this node: " + print_node(node_a_anti_node))
        logger.debug("Found this node: " + print_node(node_b_anti_node))

    return anti_nodes


def get_antinodes_v2(node_a: tuple[int, int], node_b: tuple[int, int]):
    """
    An antinode is defined to be a point where two nodes line up,
    and the distance from both nodes is double of another.

    So nodes can either be lined up vertically, horizontally, or lastly in a diagonal.
    If antinodes exist, returns their respective positions.

    """

    antinodes: list = []

    node_a_anti_node_offset = (node_a[0] - node_b[0], node_a[1] - node_b[1])
    node_b_anti_node_offset = (node_b[0] - node_a[0], node_b[1] - node_a[1])

    node_a_anti_node = (
        node_a[0] + node_a_anti_node_offset[0],
        node_a[1] + node_a_anti_node_offset[1],
    )

    # TODO: should turn this into a function
    while valid_pos(node_a_anti_node):
        antinodes.append(node_a_anti_node)
        node_a_anti_node = (
            node_a_anti_node[0] + node_a_anti_node_offset[0],
            node_a_anti_node[1] + node_a_anti_node_offset[1],
        )

    node_b_anti_node = (
        node_b[0] + node_b_anti_node_offset[0],
        node_b[1] + node_b_anti_node_offset[1],
    )

    while valid_pos(node_b_anti_node):
        antinodes.append(node_b_anti_node)
        node_b_anti_node = (
            node_b_anti_node[0] + node_b_anti_node_offset[0],
            node_b_anti_node[1] + node_b_anti_node_offset[1],
        )

    return antinodes


def get_antinode_cnt_v1(symbols: defaultdict) -> int:
    """
    This function is the main function for solving part 1.
    This runs in O(n^2) since we have to compare every
    cell (antenna in this context) to every other cell
    that has the same antenna.

    Refer to get_antinodes_v1 for key intuition.

    """
    antinodes: set = set()

    for symbol, positions in symbols.items():
        logger.debug(f"Looking at this symbol: {symbol}")
        for i in range(len(positions)):
            node_a = positions[i]
            for j in range(i + 1, len(positions)):
                node_b = positions[j]
                found_antinodes = get_antinodes_v1(node_a, node_b)
                for antinode in found_antinodes:
                    antinodes.add(antinode)

    if logger.getEffectiveLevel() == logging.DEBUG:
        for antinode in sorted(antinodes):
            logger.debug((print_node(antinode)))

    return len(antinodes)


def get_antinode_cnt_v2(symbols: defaultdict) -> int:
    """
    This function solves part 2.
    This runs in the same time complexity but runs
    get_antinodes_v2 instead.

    Refer to get_antinodes_v2 for key intuition.
    """

    antinodes: set = set()

    for symbol, positions in symbols.items():
        logger.debug(f"Looking at this symbol: {symbol}")
        # As long as there is 2 or more towers, every tower is a antinode
        if len(positions) >= 2:
            for node in positions:
                antinodes.add(node)
        for i in range(len(positions)):
            node_a = positions[i]
            for j in range(i + 1, len(positions)):
                node_b = positions[j]
                found_antinodes = get_antinodes_v2(node_a, node_b)
                for antinode in found_antinodes:
                    antinodes.add(antinode)

    if logger.getEffectiveLevel() == logging.DEBUG:
        for antinode in sorted(antinodes):
            logger.debug((print_node(antinode)))

    return len(antinodes)


def main():
    file_path = get_args("Solution for day 8 of Advent of Code 2024.", "day8")
    lines = get_input(file_path)

    symbols = get_symbols(lines)

    antinode_cnt = get_antinode_cnt_v1(symbols)
    print(f"The amount of unique antinode for part 1 is: {antinode_cnt}")

    antinode_cnt_v2 = get_antinode_cnt_v2(symbols)
    print(f"The amount of unique antinodes for part 2 is: {antinode_cnt_v2}")


if __name__ == "__main__":
    main()
