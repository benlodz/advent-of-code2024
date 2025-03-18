from common import *
from typing import List, Tuple, Set, Dict, Deque, DefaultDict, Union
from pathlib import Path
from collections import deque, defaultdict
import logging
import heapq
import copy
from itertools import product, permutations
from functools import cache
import re
from math import floor


def get_connected(lines: List[str]) -> int:
    global logger

    # build adj list
    adj: DefaultDict[str, List[str]] = defaultdict(list)
    for src, dst in [line.split("-") for line in lines]:
        adj[src].append(dst)
        adj[dst].append(src)

    connected: Set = set()
    cnt = 0

    # O(n^3) to generate all combinations
    for i in adj.keys():
        for j in adj[i]:
            # prevent loopback
            if j == i:
                continue
            for k in adj[j]:
                # prevent loopback
                if i == k or j == k:
                    continue
                if ("t" == i[0] or "t" in j[0] or "t" in k[0]) and k in adj[i]:
                    # logger.debug(f"found this combination: {i + j + k}")
                    combinations = list(permutations((i, j, k)))
                    if not any(
                        combination in connected for combination in combinations
                    ):
                        connected.update(combinations)
                        cnt += 1

    logger.debug(connected)
    return cnt


def get_lan_party_password(lines: List[str]) -> str:
    global logger

    # build adj list and collect vertices
    adj: DefaultDict[str, List[str]] = defaultdict(list)
    for src, dst in [line.split("-") for line in lines]:
        adj[src].append(dst)
        adj[dst].append(src)

    def bron_kerbosch(R, P, X, graph):
        if not P and not X:
            yield R
        while P:
            v = P.pop()
            yield from bron_kerbosch(
                R.union({v}), P.intersection(graph[v]), X.intersection(graph[v]), graph
            )
            X.add(v)

    graph = {k: set(adj[k]) for k in adj.keys()}
    all_cliques = list(bron_kerbosch(set(), set(graph.keys()), set(), graph))

    max_clique = set()
    for clique in all_cliques:
        if len(clique) > len(max_clique):
            max_clique = clique

    lan_party = sorted(list(max_clique))

    return ",".join(lan_party)


def solve(file_path: Path, logging_level: int) -> None:
    global logger
    lines = read_file(file_path)

    t_connected = get_connected(lines)
    logger.info(
        f"For part 1, there are {t_connected} computers that are connected with the letter t."
    )

    logger.info(get_lan_party_password(lines))


def main():
    file_path: str
    day: str = "day23"
    file_path, logging_level = quick_parse(day)
    global logger
    logger = get_logger(day, logging_level)
    solve(Path(file_path), logging_level)


if __name__ == "__main__":
    main()

"""
2'389 too high

am,bq,bs,cz,ek,jd,pm,ri,vc,vp,xg,xu,zi # wrong
bl,rr,kk,ch,tb,vw,bg,fv,pv,fn,gd,jn,lk # wrong
"""
