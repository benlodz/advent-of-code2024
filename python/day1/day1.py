from heapq import *
from collections import Counter
import copy

# load input
with open("day1_input.txt", "r") as f:
    lines = f.read().splitlines()
    f.close()

# separate numbers into two lists
l1, l2 = [], []
for line in lines:
    n1, n2 = line.split()
    l1.append(int(n1))
    l2.append(int(n2))

h1, h2 = copy.deepcopy(l1), copy.deepcopy(l2)
heapify(h1)
heapify(h2)
distance = 0
for _ in range(len(h1)):
    distance += abs(heappop(h1) - heappop(h2))

print(f"Distance between lists: {distance}")

cnt = Counter(l2)
sim_score = 0
for n in l1:
    if n in cnt:
        sim_score += n * cnt[n]

print(f"Similarity Score: {sim_score}")


def get_similarity_score() -> int:
    pass


def get_distance() -> int:
    pass


def main():
    pass


if __name__ == "__main__":
    main()
