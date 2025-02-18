from common import *
from typing import List, Tuple, Set, Dict, Deque
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy


def read_lines(lines: List[str]) -> Tuple[int, List[int]]:
    A = int(lines[0].split()[-1])

    last_line: str = lines[-1]
    i: int = 0
    while not last_line[i].isdecimal():
        i += 1

    program: List[int] = [int(c) for c in last_line[i:].split(",")]
    return (A, program)


def solve_program(lines: List[str]) -> None:
    A: int
    program: List[int]
    A, program = read_lines(lines)
    output: List[int] = []

    B: int = 0
    C: int = 0

    opcode: int
    operand: int
    ip: int = 0
    while ip < len(program):

        opcode = program[ip]
        operand = program[ip + 1]
        if operand == 4:
            operand = A
        elif operand == 5:
            operand = B
        elif operand == 6:
            operand = C

        match opcode:
            case 0:
                # adv: integer division of a register with 2^operand
                A = A // (2**operand)
            case 1:
                # bxl: bitwise XOR of B register and operand
                B = B ^ operand
            case 2:
                # bst: write operand mod 8 to register
                B = operand % 8
            case 3:
                # jnz: move IP to literal operand (probably 0)
                if A:
                    ip = operand
            case 4:
                # bxc: bitwise XOR of register B and C, put into B
                B = B ^ C
            case 5:
                # out: mod 8 of operand and then prints it
                output.append(operand % 8)
            case 6:
                # bdv: works like adv except for B register
                B = B // (2**operand)
            case 7:
                # cdv: works like adv except for C register
                C = C // (2**operand)
        if opcode != 3 or not A:
            ip += 2
    return output


def get_lowest_a(lines: List[str]) -> None:
    A: int
    program: List[int]
    A, program = read_lines(lines)

    def recursive(a: int, target_ptr: int):
        print(f"Enterting recursive call")
        print(f"a: {a}, ptr:{target_ptr}")

        if target_ptr == -1:
            print("*" * 10)
            print("bottomed out")
            print(a)
            print("*" * 10)
            return a

        A: int
        for n in range(8):
            A = (a << 3) | n
            print(f"A val: {A}")
            B: int = 0
            C: int = 0

            opcode: int
            operand: int
            ip: int = 0
            output = None
            while ip < len(program):

                opcode = program[ip]
                operand = program[ip + 1]
                if operand == 4:
                    operand = A
                elif operand == 5:
                    operand = B
                elif operand == 6:
                    operand = C

                match opcode:
                    case 0:
                        # adv: integer division of a register with 2^operand
                        A = A // (2**operand)
                    case 1:
                        # bxl: bitwise XOR of B register and operand
                        B = B ^ operand
                    case 2:
                        # bst: write operand mod 8 to register
                        B = operand % 8
                    case 3:
                        raise ValueError("Should never get into the loop")
                    case 4:
                        # bxc: bitwise XOR of register B and C, put into B
                        B = B ^ C
                    case 5:
                        # out: mod 8 of operand and then prints it
                        output = operand % 8
                        print(f"got this {output}")
                    case 6:
                        # bdv: works like adv except for B register
                        B = A // (2**operand)
                    case 7:
                        # cdv: works like adv except for C register
                        C = A // (2**operand)

                if output is not None and output == program[target_ptr]:
                    print("A register when recursive: ", A)
                    res = recursive(((a << 3) | n), target_ptr - 1)
                    if res != 0:
                        return res
                    else:
                        break
                if output is not None:
                    break

                if opcode != 3 or not A:
                    ip += 2
        return 0

    return recursive(0, len(program) - 1)


def solve(file_path: Path, logging_level: int) -> None:
    lines: List[str] = read_file(file_path)
    output: List[int] = solve_program(lines)
    print(f"For part 1, the output is: ", output)

    lowest_a_val = get_lowest_a(lines)
    print(lowest_a_val)


def main():
    file_path: str

    global logger
    file_path, logging_level = quick_parse("day17")
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()
