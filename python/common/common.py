import logging

# Global error logger
error_logger: logging.Logger
error_logger = logging.Logger("Error Logger")


def read_file(file_path: str) -> list[str]:
    try:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
            file.close()
    except FileNotFoundError:
        error_logger.error(f"Failed to find at this path: {file_path}")
    except IOError:
        error_logger.error(f"An error occurred while tr")
    except Exception as e:
        error_logger.error(f"An unexpected error occurred: {str(e)}")
    return lines
