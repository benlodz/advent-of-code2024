import logging
import argparse
from pathlib import Path
from functools import reduce
from collections import Counter, defaultdict, deque
import copy

# Global error logger
error_logger: logging.Logger
error_logger = logging.Logger("Error Logger")

# Constants
DIRECTIONS_4D: tuple = ((0, 1), (1, 0), (-1, 0), (0, -1))

DIRECTIONS_8D: tuple = (
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
    (1, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
)


def read_file(file_path: Path) -> list[str]:
    """
    Reads a file and returns its contents as a list of strings.

    Args:
        file_path (Path): The path to the file to be read. This should be an instance
                          of `pathlib.Path`, which allows for more robust handling
                          of filesystem paths across different operating systems.

    Returns:
        list[str]: A list of strings, where each string is a line from the file.
                   If an error occurs while reading the file, an empty list is returned.

    Raises:
        FileNotFoundError: If the specified file does not exist at the given path.
        IOError: If an error occurs during file reading (e.g., permission issues).
        Exception: Logs unexpected errors that may occur during file operations.
    """

    if not file_path.is_file():
        raise FileNotFoundError("Failed to find input!")

    try:
        with file_path.open() as file:
            lines = file.read().splitlines()
            file.close()
    except FileNotFoundError:
        error_logger.error(f"Failed to find at this path: {file_path}")
    except IOError:
        error_logger.error(
            f"An error occurred while trying to read the file: {file_path}"
        )
    except Exception as e:
        error_logger.error(f"An unexpected error occurred: {str(e)}")

    if lines is None:
        raise ValueError("Failed to get lines?")
    return lines
