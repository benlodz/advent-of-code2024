from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict, Union
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
from itertools import product, permutations
from functools import cache
import re
from math import floor

logger: logging.Logger


def get_z_decimal(lines: List[str]) -> int:
    global logger

    """
    I think a wire can have one gate to it, or at most two dependencies
    so we do a topological sort and then if a wire does not have a value
    we simply, evaluate it. 

    Wires cannot change values only receive them.

    Wires can be a dependency for multiple wires. 
    """

    # parse beginning and get initial values for wires
    wire_values: Dict[str, int] = {}
    wires: Set = set()
    i = 0
    while line := lines[i]:
        split: List[str] = line.split(":")
        wire: str = split[0]
        wires.add(wire)
        val: int = int(split[1].strip())
        wire_values[wire] = val
        i += 1

    logger.debug("Starting values for wires")
    for wire in wires:
        logger.debug(f"wire:{wire}:{wire_values[wire]}")

    # get edges from vertices, they will also contain a second property (the gate)
    i += 1
    # key: src value: (dst, gate)
    adj: DefaultDict[str, List[str]] = defaultdict(list)

    # wire / vertice -> (gate, left, right)
    wire_gate: Dict[str, Tuple[str, str, str]] = {}
    while i < len(lines) and (line := lines[i]):
        logger.debug(f"got line: {line}")
        matches = re.findall(r"\b\w+\b", line)
        left, gate, right, dst = matches

        # connect wires
        adj[left].append(dst)
        adj[right].append(dst)

        # attach gate to node / wire
        wire_gate[dst] = (gate, left, right)

        # add potential wires / vertices
        wires.add(left)
        wires.add(right)
        wires.add(dst)

        i += 1

    # perform topological sort

    visited: Set = set()
    stack: List = []

    def dfs(node: str) -> None:

        # exit if we've visited node already
        if node in visited:
            return

        visited.add(node)
        for nei in adj[node]:
            dfs(nei)
        stack.append(node)

    for wire in wires:
        dfs(wire)
    topological_order = stack[::-1]
    logger.debug(f"Topological ordering:{topological_order}")

    for wire in topological_order:

        # skip wires with initial values
        if wire in wire_values:
            continue

        gate, dep1, dep2 = wire_gate[wire]
        try:
            if gate == "AND":
                wire_values[wire] = wire_values[dep1] & wire_values[dep2]
            elif gate == "OR":
                wire_values[wire] = wire_values[dep1] | wire_values[dep2]
            elif gate == "XOR":
                wire_values[wire] = wire_values[dep1] ^ wire_values[dep2]
        except:
            logger.debug("A value was missing??")

    # logger.debug(wire_values)
    z_decimal: int = 0
    for wire in wires:
        # logger.debug(f"Looking at wire:{wire}")
        if wire[0] == "z" and wire_values[wire]:
            z_decimal += 2 ** (int(wire[1:]))

    return z_decimal


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    z_decimal: int = get_z_decimal(lines)
    logger.info(
        f"For part 1, the decimal number produced from the z wires is: {z_decimal}"
    )


def main():
    file_path: str
    day: str = "day24"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
