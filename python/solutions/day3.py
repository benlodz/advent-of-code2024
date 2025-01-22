import re
import argparse



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help="Solves Day 3 of advent of code",
        type=str,
    )
    args = parser.parse_args()

    return args.input if args.input else "day3_input.txt"

def get_line(file_path: str) -> str:
    with open(file_path, 'r') as f:
        line = f.read()
        f.close()
    return line

def process_line(line: str) -> str:
    """
    If we encounter do() that means we can accept characters.
    Otherwise, once we get to don't(), we should reject characters,
    until we find another do().

    We assume that we're consuming characters at the beginning.
    """    

    line_parts = []

    dont_offset = 7
    do_offset = 4
    start = 0
    enabled = True
    for i, c in enumerate(line):
        if c == 'd' and enabled and line[i: i + dont_offset] == "don't()":
            line_parts.append(line[start:i])
            enabled = False
        elif c == 'd' and not enabled and line[i: i + do_offset] == "do()":
            enabled= True
            start = i
    
    if enabled:
        line_parts.append(line[start:])
    
    return "".join(line_parts)




def main():
    file_path = get_args()
    line = get_line(file_path)

    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)

    total = 0
    for match in matches:
        x, y = match
        total += int(x) * int(y)
    
    print(f"For part 1, the total is {total}")
    new_input = process_line(line)
    # print(new_input)

    new_total = 0
    new_matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", new_input)

    matches_list = set(matches)
    new_matches_list = set(new_matches)
    
    print(f"amount of matches in part 1: {len(matches_list)}")
    print(f"amount of matches in part 2: {len(new_matches_list)}")

    # assert(len(matches) >= len(new_matches_list))
    for match in new_matches:
        x, y = match
        # print(f"adding {x} and {y} to the total")
        new_total += int(x) * int(y)
    
    print(f"For part 2, the total is {new_total}")

    assert( new_total <= total)


main()
