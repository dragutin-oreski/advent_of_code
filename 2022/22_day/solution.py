from typing import Iterator, Optional


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _get_grid(reader):
    grid = []

    max_len = 0
    for line in reader:
        if line.strip() == "":
            break
        row = [char for char in line]
        grid.append(row)
        if len(row) >= max_len:
            max_len = len(row)

    for row in grid:
        while len(row) < max_len:
            row.append(' ')

    return grid


def _get_instructions(reader):
    instructions: str = next(reader)

    numbers = ''
    for idx in range(len(instructions)):
        if not instructions[idx].isnumeric():
            if numbers:
                yield int(numbers)
                numbers = ''
            yield instructions[idx]
        else:
            numbers = f"{numbers}{instructions[idx]}"
    yield int(numbers)


def _get_next_position(m, n, grid, direction, wrap):
    if not wrap:
        if direction == '>':
            while True:
                n = (n + 1) % len(grid[0])
                if grid[m][n] != ' ':
                    return m, n, direction
        if direction == '<':
            while True:
                n = (n - 1) % len(grid[0])
                if grid[m][n] != ' ':
                    return m, n, direction
        if direction == 'v':
            while True:
                m = (m + 1) % len(grid)
                if grid[m][n] != ' ':
                    return m, n, direction
        if direction == '^':
            while True:
                m = (m - 1) % len(grid)
                if grid[m][n] != ' ':
                    return m, n, direction

    if direction == '>':
        _n = n + 1
        if _n < len(grid[0]) and grid[m][_n] != ' ':
            return m, _n, direction
        if _n == len(grid[0]):
            return 149 - m, n - 50, "<"
        if 50 <= m <= 99:
            return 49, 50 + m, "^"
        if 100 <= m <= 149:
            return 149 - m, 149, "<"
        if 150 <= m <= 199:
            return 149, m - 100, "^"

    if direction == 'v':
        _m = m + 1
        if _m < len(grid) and grid[_m][n] != ' ':
            return _m, n, direction
        if m == 199:
            return 0, n + 100, "v"
        if m == 149:
            return n + 100, 49, "<"
        if m == 49:
            return n - 50, 99, "<"

    if direction == '<':
        _n = n - 1
        if _n >= 0 and grid[m][_n] != ' ':
            return m, _n, direction
        if 0 <= m <= 49:
            return 149 - m, 0, ">"
        if 50 <= m <= 99:
            return 100, m - 50, "v"
        if 100 <= m <= 149:
            return 149 - m, 50, ">"
        if 149 <= m <= 199:
            return 0, m - 100, "v"

    if direction == '^':
        _m = m - 1
        if _m >= 0 and grid[_m][n] != ' ':
            return _m, n, direction
        if 0 <= n <= 49:
            return 50 + n, 50, ">"
        if 50 <= n <= 99:
            return 100 + n, 0, ">"
        if 100 <= n <= 149:
            return 199, n - 100, "^"


def _get_new_direction(curent_direction, change):
    directions = ['^', '>', 'v', '<']

    idx = directions.index(curent_direction)
    if change == 'R':
        idx += 1
    else:
        idx -= 1
    idx = idx % len(directions)
    return directions[idx]


def task(wrap: bool = False):
    reader = _read_input_file()
    grid = _get_grid(reader)

    direction = '>'
    m, n = 0, 0
    m, n, direction = _get_next_position(m, n, grid, direction, False)
    for idx, instruction in enumerate(_get_instructions(reader)):
        if isinstance(instruction, str):
            direction = _get_new_direction(direction, instruction)
            continue
        number = instruction
        while number > 0:
            next_m, next_n, next_direction = _get_next_position(m, n, grid, direction, wrap)
            if grid[next_m][next_n] != '#':
                grid[m][n] = direction
                m = next_m
                n = next_n
                direction = next_direction
                number -= 1
            else:
                break

    if direction == '>':
        direction_value = 0
    if direction == 'v':
        direction_value = 1
    if direction == '<':
        direction_value = 2
    if direction == '^':
        direction_value = 3

    return 1000 * (m + 1) + 4 * (n + 1) + direction_value


if __name__ == "__main__":
    print(task())
    print(task(wrap=True))
