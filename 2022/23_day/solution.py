from collections import defaultdict, Counter
from typing import Iterator, Optional, List


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _ensure_buffer(grid: List[List[str]]) -> List[List[str]]:

    for char in grid[0]:
        if char == '#':
            grid.insert(0, ['.'] * len(grid[0]))
            break

    for char in grid[-1]:
        if char == '#':
            grid.append(['.'] * len(grid[0]))
            break

    for idx in range(len(grid)):
        if grid[idx][-1] == '#':
            for line in grid:
                line.append('.')
            break

    for idx in range(len(grid)):
        if grid[idx][0] == '#':
            for line in grid:
                line.insert(0, '.')
            break

    return grid


def _remove_buffer(grid: List[List[str]]) -> List[List[str]]:

    if set(grid[0]) == {'.'}:
        grid.pop(0)
    if set(grid[-1]) == {'.'}:
        grid.pop()

    chars = {grid[idx][-1] for idx in range(len(grid))}
    if chars == {'.'}:
        for line in grid:
            line.pop()

    chars = {grid[idx][0] for idx in range(len(grid))}
    if chars == {'.'}:
        for line in grid:
            line.pop(0)

    return grid


def _get_grid() -> List[List[str]]:
    grid = []
    for line in _read_input_file():
        grid.append([char for char in line])

    return grid


conditions = [
    "grid[m - 1][n - 1] == '.' and grid[m - 1][n] == '.' and grid[m - 1][n + 1] == '.'",
    "grid[m + 1][n - 1] == '.' and grid[m + 1][n] == '.' and grid[m + 1][n + 1] == '.'",
    "grid[m - 1][n - 1] == '.' and grid[m][n - 1] == '.' and grid[m + 1][n - 1] == '.'",
    "grid[m - 1][n + 1] == '.' and grid[m][n + 1] == '.' and grid[m + 1][n + 1] == '.'",
]
steps = [
    'proposals[(m - 1, n)].append((m, n))',
    'proposals[(m + 1, n)].append((m, n))',
    'proposals[(m, n - 1)].append((m, n))',
    'proposals[(m, n + 1)].append((m, n))',
]


def task(rounds: int) -> int:
    grid = _get_grid()

    for idx in range(rounds):

        grid = _ensure_buffer(grid)
        proposals = defaultdict(list)
        for m in range(len(grid)):
            for n in range(len(grid[0])):
                if grid[m][n] == '.':
                    continue
                if grid[m - 1][n - 1] == '.' and grid[m - 1][n] == '.' and grid[m - 1][n + 1] == '.' \
                    and grid[m][n - 1] == '.' and grid[m][n + 1] == '.' \
                    and grid[m + 1][n - 1] == '.' and grid[m + 1][n] == '.' and grid[m + 1][n + 1] == '.':
                    proposals[(m, n)].append((m, n))

                elif eval(conditions[idx % len(conditions)]):
                    eval(steps[(idx + 0) % len(conditions)])
                elif eval(conditions[(idx + 1) % len(conditions)]):
                    eval(steps[(idx + 1) % len(conditions)])
                elif eval(conditions[(idx + 2) % len(conditions)]):
                    eval(steps[(idx + 2) % len(conditions)])
                elif eval(conditions[(idx + 3) % len(conditions)]):
                    eval(steps[(idx + 3) % len(conditions)])
                else:
                    proposals[(m, n)].append((m, n))
        exit = True
        for destination, origin in proposals.items():
            if len(origin) > 1 or destination != origin[0]:
                exit = False
                break
        if exit:
            return idx + 1

        for destination, origin in proposals.items():
            if len(origin) == 1 and destination != origin[0]:
                m, n = destination
                grid[m][n] = '#'
                m, n = origin[0]
                grid[m][n] = '.'

    grid = _remove_buffer(grid)
    c = Counter()
    [c.update(line) for line in grid]
    return c['.']


if __name__ == "__main__":
    print(task(10))
    print(task(10_000))
