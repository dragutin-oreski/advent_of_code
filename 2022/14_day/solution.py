from typing import Iterator, Optional, List


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _read_line():
    for line in _read_input_file():
        yield [[int(x) for x in rec.split(',')] for rec in line.split(' -> ')]


def _get_limits():
    max_x = 0
    max_y = 500
    min_y = 500
    for pair in _read_line():
        for y, x in pair:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y

    return max_x, min_y, max_y


def _create_grid(max_x: int, min_y: int, max_y: int) -> List[List[str]]:
    m_dimension = max_x + 1
    n_dimension = max_y - min_y + 1

    matrix = [['.' for _ in range(n_dimension)] for _ in range(m_dimension)]

    # print(' ', [i + min_y for i in range(n_dimension)])
    # for idx, line in enumerate(matrix):
    #     print(idx, line)

    return matrix


def _draw_lines(matrix, min_y):

    for line in _read_line():
        for idx in range(len(line) - 1):
            left_tuple = line[idx]
            right_tuple = line[idx + 1]
            start_n = min(left_tuple[0] - min_y, right_tuple[0] - min_y)
            end_n = max(left_tuple[0] - min_y, right_tuple[0] - min_y)
            start_m = min(left_tuple[1], right_tuple[1])
            end_m = max(left_tuple[1], right_tuple[1])

            for m in range(start_m, end_m + 1):
                for n in range(start_n, end_n + 1):
                    matrix[m][n + 1] = "#"

    return matrix


def produce_sand(do_print: bool = False) -> int:
    max_x, min_y, max_y = _get_limits()
    n_dimension = max_y - min_y + 1
    matrix = _create_grid(max_x, min_y - 1, max_y + 1)
    _draw_lines(matrix, min_y)

    if do_print:
        print(' ', [i + min_y - 1 for i in range(n_dimension + 2)])
        for idx, line_matrix in enumerate(matrix):
            print(idx, line_matrix)

    ans = 0
    while True:
        sand_m, sand_n = 0, 500 - min_y + 1
        matrix[sand_m][sand_n] = 'o'
        while True:
            matrix[sand_m][sand_n] = '.'
            sand_m += 1
            if sand_m > max_x:
                matrix[sand_m - 1][sand_n] = 'o'
                break
            if matrix[sand_m][sand_n] == '.':
                matrix[sand_m][sand_n] = 'o'
            elif matrix[sand_m][sand_n - 1] == '.':
                sand_n -= 1
                matrix[sand_m][sand_n] = 'o'
            elif matrix[sand_m][sand_n + 1] == '.':
                sand_n += 1
                matrix[sand_m][sand_n] = 'o'
            else:
                matrix[sand_m - 1][sand_n] = 'o'
                break
        if sand_m > max_x:
            break
        ans += 1

    if do_print:
        print(' ', [i + min_y - 1 for i in range(n_dimension + 2)])
        for idx, line_matrix in enumerate(matrix):
            print(idx, line_matrix)
    return ans


def produce_sand_on_top(do_print: bool = False) -> int:
    max_x, min_y, max_y = _get_limits()
    max_x += 2
    min_y = min(min_y, 500 - max_x)
    max_y = max(max_y, 500 + max_x)
    n_dimension = max_y - min_y + 1
    matrix = _create_grid(max_x, min_y - 1, max_y + 1)
    _draw_lines(matrix, min_y)
    matrix[-1] = ['#'] * (n_dimension + 2)

    if do_print:
        print(' ', [i + min_y - 1 for i in range(n_dimension + 2)])
        for idx, line_matrix in enumerate(matrix):
            print(idx, line_matrix)

    ans = 0
    while True:
        sand_m, sand_n = 0, 500 - min_y + 1
        if matrix[sand_m][sand_n] == 'o':
            break
        matrix[sand_m][sand_n] = 'o'
        while True:
            matrix[sand_m][sand_n] = '.'
            sand_m += 1
            if matrix[sand_m][sand_n] == '.':
                matrix[sand_m][sand_n] = 'o'
            elif (sand_n - 1) >= 0 and matrix[sand_m][sand_n - 1] == '.':
                sand_n -= 1
                matrix[sand_m][sand_n] = 'o'
            elif matrix[sand_m][sand_n + 1] == '.':
                sand_n += 1
                matrix[sand_m][sand_n] = 'o'
            else:
                matrix[sand_m - 1][sand_n] = 'o'
                break
        if sand_m == 0:
            break
        ans += 1

    if do_print:
        print(' ', [i + min_y - 1 for i in range(n_dimension + 2)])
        for idx, line_matrix in enumerate(matrix):
            print(idx, line_matrix)
    return ans


if __name__ == "__main__":
    print(produce_sand(do_print=False))
    print(produce_sand_on_top(do_print=False))
