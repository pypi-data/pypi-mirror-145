from typing import List

import collections
import numpy as np


def is_connected(nnlist: List[List[int]]) -> bool:
    nnodes = len(nnlist)
    visited = np.full(nnodes, False)
    nvisited = 1
    visited[0] = True
    stack = collections.deque([0])
    while len(stack) > 0:
        node = stack.pop()
        neighbors = [n for n in nnlist[node] if not visited[n]]
        visited[neighbors] = True
        stack.extend(neighbors)
        nvisited += len(neighbors)

    return nvisited == nnodes


def is_bidirectional(nnlist: List[List[int]]) -> bool:
    for i in range(len(nnlist)):
        for j in nnlist[i]:
            if i not in nnlist[j]:
                return False
    return True


if __name__ == "__main__":
    filename = "./neighborlist.txt"
    nnlist = []
    with open(filename) as f:
        for line in f:
            words = line.split()
            nn = [int(w) for w in words[1:]]
            nnlist.append(nn)
    print(is_connected(nnlist))
