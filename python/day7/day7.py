import argparse
import logging
import array

# type annotation for global logger
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
        lines = f.read().splitlines()
        f.close()
    return lines


def concat_operation_int(x: int, y: int) -> int:
    """
    In part 2, we're given a new type of operator: |
    This operator concats two numbers like so
    12 | 3 = 123
    """

    # concatation between strings is fairly trivial
    # but we'll compare performance between ints and str's
    y_len: int = 0
    temp: int = y
    while temp:
        temp = temp // 10
        y_len += 1

    # make space in x to add y
    x *= 10**y_len

    return x + y


def process_lines(lines: list[str]) -> list[list[int]]:
    """
    In this problem our input is given in the form of:
    190: 10 19

    We process these lines and put them into a list.
    Where the first index represents the target and the rest is the equation
    """

    equations = []
    for line in lines:
        equation = []
        split_idx = line.find(":")
        # target is the first idx
        equation.append(int(line[:split_idx]))
        # extend by the rest of the input
        equation.extend([int(n) for n in line[split_idx + 1 :].split()])
        equations.append(equation)

    return equations


def is_valid_equation_v1(target: int, equation: list[int]) -> bool:
    """
    This is the Dynamic programming solution used to solve part 1.
    We return a 1 if we found a path that reaches our target.
    Otherwise, return 0 if we go too far.

    We do an OR operation on both paths and store it in the cache.

    TODO: Rewrite this function using bottom up tabulation

    """

    DP: dict = {}

    def dfs(i: int, total: int) -> bool:

        # cache hit
        if (i, total) in DP:
            return DP[(i, total)]

        if total == target:
            return True

        # base case
        if i == len(equation) or total > target:
            return False

        add_path = dfs(i + 1, total + equation[i])
        multiply_path = dfs(i + 1, total * equation[i])

        DP[(i, total)] = add_path or multiply_path
        return DP[(i, total)]

    return dfs(0, 0)


def is_valid_equation_v2(target: int, equation: list[int]) -> bool:
    """
    The difference here is that we now have a third split in our decision tree
    Making the recursive solution O(3^n).

    However, the runtime is saved by dynamic programming as it's still a 2D cache.

    """

    DP: dict = {}

    def dfs(i: int, total: int) -> bool:
        logger.debug(f"At idx:{i}, total:{total}")

        if (i, total) in DP:
            return DP[(i, total)]

        if total > target:
            return False

        # base case
        if i == len(equation):
            return True if total == target else False

        logger.debug("Exploring Add path")
        # add it
        add_path = dfs(i + 1, total + equation[i])

        logger.debug("Exploring Multiply Path")
        # multiply it
        multiply_path = dfs(i + 1, total * equation[i])

        logger.debug("Exploring Concat path")
        # concat it
        concat_path = dfs(i + 1, concat_operation_int(total, equation[i]))

        DP[(i, total)] = add_path or multiply_path or concat_path
        return DP[(i, total)]

    return dfs(0, 0)


def get_valid_equation_cnt_v1(equations: list[list[int]]) -> tuple[int, set[int]]:
    """
    This solves part 1 of day 7. This will iterate over the input
    and return both the count and the index's in which it's valid.

    We don't actually need to return the indices. However, it'll
    be useful for when we do part 2 since we won't have to consider
    equations that we already know have a valid solution with just
    addition and multiplication operators.
    """

    valid_equation_total: int = 0

    # this variable will save us calculations for part 2
    valid_indices: set = set()
    for i, equation in enumerate(equations):
        logger.debug(f"Examining this equation: {equation}")

        # 0 idx is the target, the rest is the equation.
        if is_valid_equation_v1(equation[0], equation[1:]):
            valid_equation_total += equation[0]
            valid_indices.add(i)

    return (valid_equation_total, valid_indices)


def get_valid_equation_cnt_v2(
    equations: list[list[int]], valid_indices: set[int]
) -> int:
    """
    This is for part 2 where now we include the third operation.
    Otherwise, it works pretty much the same.
    """

    logger.debug("Determining the total sum with concat operation.")
    valid_equation_total: int = 0
    for i, equation in enumerate(equations):
        if i in valid_indices:
            continue
        logger.debug(f"Examining this equation: {equation}")
        target = equation[0]
        if is_valid_equation_v2(target, equation[1:]):
            logger.debug("This equation was valid")
            valid_equation_total += target

    return valid_equation_total


def main():
    file_path: str = get_args("Solution for day 7 of advent of code 2024.", "day7")
    lines = get_input(file_path)

    equations = process_lines(lines)

    # this is how you unpack tuples with type annotations
    valid_equations_sum: int
    valid_indices: set
    valid_equations_sum, valid_indices = get_valid_equation_cnt_v1(equations)

    print(f"The sum of all valid equations for part 1 is: {valid_equations_sum}")

    valid_equations_total_with_concat: int = get_valid_equation_cnt_v2(
        equations, valid_indices
    )

    print(
        f"The sum of valid equations with concat operations is: {valid_equations_sum + valid_equations_total_with_concat}"
    )


if __name__ == "__main__":
    main()
