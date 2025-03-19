from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict, Union
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
from itertools import product, permutations, combinations
from dataclasses import dataclass
from functools import cache
import re
from math import floor

logger: logging.Logger


"""
For Part 2, it was really challenging and I wrote this code learning from
0xdf's approach. Thank you!
"""


@dataclass
class Connection:
    inputs: list[str]  # wires needed to form wire in output
    op: str  # operation performed XOR, AND, OR
    output: str  # wire being formed


operations = {
    "OR": lambda x1, x2: x1 | x2,
    "AND": lambda x1, x2: x1 & x2,
    "XOR": lambda x1, x2: x1 ^ x2,
}


def get_wrong_gates(lines: List[str]) -> str:

    # skip the initial values since we don't actually need it
    # for this approach
    i = 0
    while line := lines[i]:
        i += 1
    i += 1

    # given some wire, get the input values needed and it's operation
    wire_map: Dict[str, Connection] = {}
    while i < len(lines) and (line := lines[i]):
        left, op, right, _, output = line.strip().split(" ")
        wire_map[output] = Connection([left, right], op, output)
        i += 1

    def run_wire(w: str, init_vals: dict[str, list[int]]) -> int:
        if w[0] in ("x", "y"):
            return init_vals[w[0]][int(w[1:])]
        con = wire_map[w]
        return operations[con.op](
            run_wire(con.inputs[0], init_vals), run_wire(con.inputs[1], init_vals)
        )

    def make_wire(letter: str, n: int) -> str:
        return letter + str(n).zfill(2)

    def swap(w1: str, w2: str) -> None:
        # swaps
        wire_map[w1], wire_map[w2] = wire_map[w2], wire_map[w1]

    def validate(n: int) -> bool:
        """
        This function works by trying every x, y, c and seeing whether this will produce
        the correct result.

        In other words, given some target n ie. z02:
        for every possible x, y, c
        """
        for x in range(2):
            for y in range(2):
                for c in range(2):
                    # all higher order bits are zero'd out
                    # this doesn't make sense at first but the list is reversed later on
                    init_x = [0] * (44 - n) + [x]
                    init_y = [0] * (44 - n) + [y]
                    if n > 0:
                        # if the carry flag is on, for example consider z5
                        # this would get z4 in our dict to be on or off
                        # subsequent lower order bits are 0'd out too
                        init_x += [c] + [0] * (n - 1)
                        init_y += [c] + [0] * (n - 1)
                    elif c > 0:
                        # in the case of z0, we cannot have a carry
                        continue

                    init_x = list(reversed(init_x))
                    init_y = list(reversed(init_y))

                    z = run_wire(make_wire("z", n), {"x": init_x, "y": init_y})
                    if z != (x + y + c) % 2:
                        return False
        return True

    def find_wire(
        op: str | None = None, input1: str | None = None, input2: str | None = None
    ) -> Connection | None:
        logger.debug(f"op:{op}\tinput1:{input1}\tinput2:{input2}")
        for wire in wire_map.values():
            if op and op != wire.op:
                continue
            if input1 and input1 not in wire.inputs:
                continue
            if input2 and input2 not in wire.inputs:
                continue
            return wire
        return None  # this should never happen

    def fix_bit_n(n: int) -> list[str]:
        """
        Valid z wires have a pattern in terms of incoming wires

        zn = nxor XOR m1
        nxor = xn XOR yn
        m1 = m2 OR prevand
        prevand = xn-1 AND yn-1
        m2 = prevxor AND (something prev)
        prevxor = xn-1 XOR yn-1

        m2 is the only value in our pattern that can have a mystery value
        """

        logger.debug(f"wire z{n} not functioning properly")
        prevand = find_wire(
            op="AND", input1=make_wire("x", n - 1), input2=make_wire("y", n - 1)
        )
        if not prevand:
            raise Exception("prevand not found!")
        prevxor = find_wire(
            op="XOR", input1=make_wire("x", n - 1), input2=make_wire("y", n - 1)
        )
        if not prevxor:
            raise Exception("prevxor not found!")
        m2 = find_wire(op="AND", input1=prevxor.output)  # type: ignore
        if not m2:
            raise Exception("Could not find m2!")
        m1 = find_wire(op="OR", input1=m2.output, input2=prevand.output)  # type: ignore
        nxor = find_wire(op="XOR", input1=make_wire("x", n), input2=make_wire("y", n))  # type: ignore
        zn = find_wire(op="XOR", input1=nxor.output, input2=m1.output)  # type: ignore

        if zn is None:
            logger.debug("zn is none!")
            # if we can't find a wire
            zn = wire_map[make_wire("z", n)]
            """
            Basically, we get the current inputs to make zn according to our wire_map / puzzle input
            then we determine which one is the odd one out from our pattern
            we then swap the wires
            """
            to_swap = list(set(zn.inputs) ^ set([nxor.output, m1.output]))  # type: ignore
            logger.debug(f"output for to_swap: {to_swap}")
        if zn.output != make_wire("z", n):
            """
            in this case, we have a mismatch in zn
            ie z10 needs to be swapped with z20
            """
            logger.debug("zn output is incorrect?")
            to_swap = [make_wire("z", n), zn.output]  # type: ignore
        swap(*to_swap)
        return to_swap

    swapped = []
    # this is only at max: 44 wires
    for i in range(45):
        logger.debug(f"Checking whether z{i} is valid.")
        # if zi fails
        if not validate(i):
            # perform swap and return swapped
            swapped.extend(fix_bit_n(i))

    return ",".join(sorted(swapped))


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

    for wire in wires:
        if len(adj[wire]) == 0 and wire[0] != "z":
            logger.debug(f"{wire} not in adj")
    return z_decimal


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    z_decimal: int = get_z_decimal(lines)
    logger.info(
        f"For part 1, the decimal number produced from the z wires is: {z_decimal}"
    )

    swapped_gates: str = get_wrong_gates(lines)
    logger.info(f"For part 2, the gates swapped are:{swapped_gates}")


def main():
    file_path: str
    day: str = "day24"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
