from functools import lru_cache
from typing import Iterator, Optional, List, Set


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


@lru_cache(1)
def _get_grid() -> List[List[str]]:
    grid = []
    reader = _read_input_file()
    next(reader)
    for line in reader:
        grid.append([char for char in line[1:-1]])

    grid.pop()

    return grid


@lru_cache(2)
def _get_arrow_positions(time: int) -> Set:
    grid = _get_grid()
    positions = set()
    for m in range(len(grid)):
        for n in range(len(grid[0])):
            if grid[m][n] == '.':
                continue
            if grid[m][n] == '>':
                positions.add((m, (n + time) % len(grid[0])))
            if grid[m][n] == '<':
                positions.add((m, (n - time) % len(grid[0])))
            if grid[m][n] == '^':
                positions.add(((m - time) % len(grid), n))
            if grid[m][n] == 'v':
                positions.add(((m + time) % len(grid), n))

    return positions


def _get_adjecant_positions(m, n, len_m, len_n) -> List:
    output = []
    if (m - 1) >= 0:
        output.append((m - 1, n))

    if (n - 1) >= 0:
        output.append((m, n - 1))
    output.append((m, n))
    if (n + 1) < len_n:
        output.append((m, n + 1))

    if (m + 1) < len_m:
        output.append((m + 1, n))

    return output


def _find_best_path(time: int, grid: List[List[str]], start_m, start_n, end_m, end_n):

    expedition_positions = set()
    while True:
        time += 1
        arrow_positions = _get_arrow_positions(time)

        if not expedition_positions:
            if (start_m, start_n) not in arrow_positions:
                expedition_positions.add((start_m, start_n))
            continue

        next_expedition_positions = set()

        for m, n in expedition_positions:
            if (m, n) == (end_m, end_n):
                return time
            for _m, _n in _get_adjecant_positions(m, n, len(grid), len(grid[0])):
                if (_m, _n) not in arrow_positions:
                    next_expedition_positions.add((_m, _n))
        expedition_positions = next_expedition_positions


def task() -> int:
    grid = _get_grid()

    time_1 = _find_best_path(time=0, grid=grid, start_m=0, start_n=0, end_m=len(grid) - 1, end_n=len(grid[0]) - 1)
    time_2 = _find_best_path(time=time_1, grid=grid, end_m=0, end_n=0, start_m=len(grid) - 1, start_n=len(grid[0]) - 1)
    return _find_best_path(time=time_2, grid=grid, start_m=0, start_n=0, end_m=len(grid) - 1, end_n=len(grid[0]) - 1)


if __name__ == "__main__":
    print(task())
