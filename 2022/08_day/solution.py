from functools import reduce
from typing import Iterator, Optional
import numpy as np


class Tree:
    def __init__(self, elem: str):
        self.elem = elem
        self.left = None
        self.right = None
        self.top = None
        self.down = None

    def __str__(self):
        return self.elem

    def __repr__(self):
        return self.elem


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def read_input():
    return np.array([list(line) for line in _read_input_file()])


def count_visibles():
    matrix = read_input()
    ans = 0

    for m in range(len(matrix)):
        for n in range(len(matrix[m])):

            if m == 0 or n == 0 or m + 1 == len(matrix) or n + 1 == len(matrix[m]):
                ans += 1
                continue

            elem = matrix[m, n]
            left = matrix[m, :n]
            up = matrix[:m, n]
            right = matrix[m, n + 1:]
            down = matrix[m + 1:, n]

            if elem > max(left) or elem > max(up) or elem > max(right) or elem > max(down):
                ans += 1

    return ans


def create_tree():
    matrix = read_input()

    node_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for m in range(len(matrix)):

        for n in range(len(matrix[m])):
            node = Tree(
                elem=matrix[m][n]
            )
            node_matrix[m][n] = node
            if m > 0:
                node_matrix[m - 1][n].down = node_matrix[m][n]
                node.top = node_matrix[m - 1][n]

            if n > 0:
                node_matrix[m][n - 1].right = node_matrix[m][n]
                node.left = node_matrix[m][n - 1]

    return node_matrix


def _get_elem(obj, attr, depth):

    if depth == 0:
        return obj

    return _get_elem(getattr(obj, attr), attr, depth - 1)


def _get_score(item, attr):
    score = 0
    depth = 1
    while True:
        candidate = _get_elem(item, attr, depth)
        if candidate == None:
            break
        if candidate.elem >= item.elem:
            score += 1
            break
        score += 1
        depth += 1

    return score


def calculate_scenic_score():
    node_matrix = create_tree()
    ans = 0

    for m in range(len(node_matrix)):
        for n in range(len(node_matrix[0])):
            item = node_matrix[m][n]

            scores = [_get_score(item, direction) for direction in ('left', 'right', 'top', 'down')]
            current = reduce((lambda x, y: x * y), scores)

            if current > ans:
                ans = current

    return ans


if __name__ == "__main__":
    print(count_visibles())
    print(calculate_scenic_score())
