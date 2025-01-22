import argparse
import time


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help="Solves Day 4 of advent of code",
        type=str,
    )
    args = parser.parse_args()

    return args.input if args.input else "day4_input.txt"


def get_input(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines


# recursive function with no DP
def get_xmas_cnt_v1(lines: list[str]) -> int:

    rows = len(lines)
    cols = len(lines[0])

    def valid_pos(r: int, c: int) -> bool:
        return (r >= 0) and (r < rows) and (c >= 0) and (c < cols)

    # we can move in all eight directions
    directions = (
        (0, 1),  # east
        (0, -1),  # west
        (1, 0),  # north
        (-1, 0),  # south
        (-1, -1),  # southwest
        (-1, 1),  # southeast
        (1, 1),  # northeast
        (1, -1),  # northwest
    )

    word = "XMAS"
    res = 0

    def dfs(r: int, c: int, i: int, direction: tuple) -> None:

        # base case
        nonlocal word
        if i == len(word):
            nonlocal res
            res += 1
            return

        if not valid_pos(r, c):
            return

        if lines[r][c] == word[i]:
            next_row = r + direction[0]
            next_column = c + direction[1]
            dfs(next_row, next_column, i + 1, direction)

        return

    for r in range(rows):
        for c in range(cols):
            for direction in directions:
                dfs(r, c, 0, direction)

    return res


def get_x_mas_cnt_v1(lines: list[str]) -> int:
    """

    A valid x-mas as an example could be this shape:
    M.S
    .A.
    M.S

    Basically we need two sides (horizontal or vertical) to match
    be composed of M or S but not both be the same

    """

    rows = len(lines)
    cols = len(lines[0])

    def valid_pos(r: int, c: int) -> bool:
        return (r >= 0) and (r < rows) and (c >= 0) and (c < cols)

    corner_cords = [
        (1, -1),  # top left
        (-1, -1),  # bottom left
        (1, 1),  # top right
        (-1, 1),  # bottom right
    ]

    # These represent the index's for the pieces
    tl = 0
    bl = 1
    tr = 2
    br = 3

    """
    valid shapes:
    M.S   S.M   S S   M.M
    .A.   .A.   .A.   .A.
    M.S   S.M   M.M   S.S
    """

    valid_letters = {"M", "S"}

    def valid_xmas(r: int, c: int) -> bool:

        # validate corner coordinates
        corner_pieces = []
        for r2, c2 in corner_cords:
            cr = r + r2
            cc = c + c2
            if not valid_pos(cr, cc):
                print("Corner cords are not valid fail")
                return False
            corner_pieces.append(lines[cr][cc])

        # First we can verify the one row has valid letters
        if (corner_pieces[tr] in valid_letters) and (
            (corner_pieces[tl] in valid_letters)
            and (corner_pieces[bl] in valid_letters)
            and (corner_pieces[br] in valid_letters)
        ):
            # Now let's check for a valid vertical X-MAS, as in example 1 and 2
            if (
                (corner_pieces[tr] != corner_pieces[tl])
                and (corner_pieces[tr] == corner_pieces[br])
                and (corner_pieces[tl] == corner_pieces[bl])
                and (corner_pieces[br] != corner_pieces[bl])
            ):
                print("found valid vertical X-MAS")
                return True
            # Now we verify for a horizontal X-MAS, as in example 3 and 4
            elif (
                (corner_pieces[tr] == corner_pieces[tl])
                and (corner_pieces[br] == corner_pieces[bl])
                and (corner_pieces[tr] != corner_pieces[br])
                and (corner_pieces[tl] != corner_pieces[bl])
            ):
                print("Found valid horizontal X-MAS")
                return True
            else:
                return False

    res = 0
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] == "A":
                print(f"Checking ({r},{c})")
                if valid_xmas(r, c):
                    res += 1

    return res


def main():
    file_path = get_args()
    lines = get_input(file_path)

    start = time.time()
    total = get_xmas_cnt_v1(lines)
    print(total)

    valid_xmas_cnt = get_x_mas_cnt_v1(lines)
    print(f"Found {valid_xmas_cnt} in input!")

    print(f"That took {time.time() - start} seconds")


main()


"""
1991 is too high


"""
