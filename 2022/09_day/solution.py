from collections import defaultdict
from typing import Iterator, Optional


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _get_tail_position(m, n, head_m, head_n):

    if n == head_n and m == head_m:
        return m, n

    if head_m == m:
        if (n + 2) == head_n:
            n += 1
            return m, n
        if (n - 2) == head_n:
            n -= 1
            return m, n

    elif head_n == n:
        if (m + 2) == head_m:
            m += 1
            return m, n
        if (m - 2) == head_m:
            m -= 1
            return m, n

    if max(abs(head_m - m), abs(head_n - n)) == 1:
        return m, n

    if head_m > m:
        m += 1
    else:
        m -= 1
    if head_n > n:
        n += 1
    else:
        n -= 1

    return m, n


def move_around():
    m, n = 0, 0
    head_m, head_n = 0, 0
    moves = defaultdict(set)
    moves[m].add(n)

    for line in _read_input_file():
        direction, steps = line.split()
        steps = int(steps)
        for step in range(steps):
            if direction == "R":
                head_n += 1
            if direction == "L":
                head_n -= 1
            if direction == "U":
                head_m += 1
            if direction == "D":
                head_m -= 1

            m, n = _get_tail_position(m, n, head_m, head_n)
            moves[m].add(n)

    return sum(len(values) for values in moves.values())


def move_around_long():
    m, n = [0] * 10, [0] * 10
    moves = defaultdict(set)
    moves[0].add(0)

    for line in _read_input_file():
        direction, steps = line.split()
        steps = int(steps)
        for step in range(steps):
            if direction == "R":
                n[-1] += 1
            if direction == "L":
                n[-1] -= 1
            if direction == "U":
                m[-1] += 1
            if direction == "D":
                m[-1] -= 1

            for idx in reversed(range(0, len(m) - 1)):
                _m, _n = _get_tail_position(m[idx], n[idx], m[idx + 1], n[idx + 1])
                m[idx] = _m
                n[idx] = _n
            moves[m[0]].add(n[0])

    return sum(len(values) for values in moves.values())


if __name__ == "__main__":
    print(move_around())
    print(move_around_long())
