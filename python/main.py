import argparse
import logging
from typing import Tuple
from solutions import *
from pathlib import Path
import importlib

# Global Logger
logger: logging.Logger

# limit for how many days
DAYS: int = 3


def get_args() -> Tuple[Path, int, bool]:
    global logger
    """
    Parse arguments

    We should check for these three things:
    Debugging
    File path
    Which problem to solve

    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="AoC 2024: Python Edition",
        description="""
        This will solve all puzzle inputs for Advent of Code 2024. 
        Files should be placed in the input folder with the format of dayN_input.txt.
        Example: day10_input.txt

        First this program will determine if the input files exist and they're
        properly formatted. If not, the program will proceed with sample inputs.
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        help="""
        Path for puzzle input. This will assumed to be the directory called inputs
        in the root directory.
        """,
        type=str,
    )

    parser.add_argument(
        "--debug",
        "-d",
        help="Specify whether to turn on debugging statements. Off by default.",
        action="store_true",
    )

    parser.add_argument(
        "--day",
        help="""
        A numerical argument to solve for a specific day.
        """,
    )

    parser.add_argument(
        "--samples",
        "-s",
        help="""
        This argument if enabled will run all sample inputs instead of
        the actual puzzle inputs. If the input folder is improperly filled,
        it will run on samples instead.
        """,
        action="store_true",
    )

    parser.add_argument(
        "--output",
        "-o",
        help="""
        TODO:
        Specify to write to a file.
        """,
        type=str,
    )

    args = parser.parse_args()

    input_path: Path

    logger = logging.getLogger("MAIN")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    level = logging.INFO

    if args.debug:
        # adds
        log_handler = logging.FileHandler("main_log.txt", mode="w")
        logger.addHandler(log_handler)
        log_handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        level = logging.DEBUG

    samples: bool = False
    if args.input:
        input_path = Path(args.input)

        if input_path.is_dir():
            logger.debug("Successfully found path for input files!")
        else:
            raise ValueError("Path is not correct!")
    elif args.samples:
        input_path = Path.cwd().parent / "samples"
        samples = True
    else:
        input_path = Path.cwd().parent / "input"

    return (input_path, level, samples)


def solve_day(day: int, input_path: Path, level: int, samples: bool) -> None:
    """
    Solve the Advent of Code problem for a specific day.

    This function attempts to dynamically import and execute
    a solution module corresponding to a given day. The input
    file path is constructed based on the provided `input_path`
    and the specified `day`.
    Args:
        day (int): The day number of the Advent of Code problem to solve.
        input_path (Path): A Path object pointing to the directory containing
                           the input files.

    Raises:
        ImportError: If the module corresponding to the given day cannot be imported.
    """
    global logger

    logger.info(f"Solving Day {day}")
    logger.info("*" * 10)

    module_path = f"solutions.day{day}"
    try:
        # Attempt to dynamically import the module for the specified day
        module = importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError("Failed to import package!")

    # Construct the path to the input file specific to this day
    input_file_path: Path
    if samples:
        input_file_path = input_path / f"day{day}_sample.txt"
    else:
        input_file_path = input_path / f"day{day}_input.txt"

    logger.debug(f"This is the path to the input file: {input_file_path}")

    # Call the solve function from the dynamically imported module
    module.solve(input_file_path, level)


def main():
    global logger
    args, level, samples = get_args()

    for day in range(1, DAYS + 1):
        solve_day(day, args, level, samples)


if __name__ == "__main__":
    main()
