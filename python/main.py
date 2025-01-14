import argparse
import logging

# Global Logger
logger: logging.Logger


def get_args() -> None:
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
        help="Specifiy whether to turn on debugging statements. Off by default.",
        action="store_true",
    )

    parser.add_argument(
        "--day",
        help="""
        Specifiy a specicific day to solve for. 
        """
    )

    parser.add_argument(
        "--samples",
        "-s",
        help="""
        This argument if enabled will run all sample inputs instead of
        the actual puzzle inputs. Off by default.
        """,
        action="store_true"
    )

    parser.add_argument(
        "--output",
        "-o",
        help="""
        Specify a file to write to.
        """,
        type=str
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug("Debugging on!")
    
    if 
    return None


def main():
    args = get_args()


if __name__ == "__main__":
    main()
