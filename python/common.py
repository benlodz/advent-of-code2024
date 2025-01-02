def get_args(desc: str, day: str):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help=desc,
        type=str,
    )
    args = parser.parse_args()

    return args.input if args.input else (day + "_input.txt")


def get_input(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines
