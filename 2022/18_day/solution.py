import functools
from collections import Counter
from typing import Iterator, Optional, List


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _get_sides(points: str) -> List:
    point_1 = tuple(int(point) for point in points.split(','))
    point_2 = (point_1[0] + 1, point_1[1], point_1[2])
    point_3 = (point_1[0] + 1, point_1[1] + 1, point_1[2])
    point_4 = (point_1[0], point_1[1] + 1, point_1[2])
    point_5 = (point_1[0], point_1[1], point_1[2] + 1)
    point_6 = (point_1[0] + 1, point_1[1], point_1[2] + 1)
    point_7 = (point_1[0] + 1, point_1[1] + 1, point_1[2] + 1)
    point_8 = (point_1[0], point_1[1] + 1, point_1[2] + 1)

    side_1 = tuple(sorted((point_1, point_2, point_3, point_4)))
    side_2 = tuple(sorted((point_1, point_2, point_5, point_6)))
    side_3 = tuple(sorted((point_5, point_6, point_8, point_7)))
    side_4 = tuple(sorted((point_4, point_3, point_8, point_7)))
    side_5 = tuple(sorted((point_1, point_5, point_4, point_8)))
    side_6 = tuple(sorted((point_2, point_6, point_3, point_7)))

    return [
        side_1,
        side_2,
        side_3,
        side_4,
        side_5,
        side_6,
    ]


def process_input():
    input_data = [line for line in _read_input_file()]
    counter = Counter()
    ans = 0
    for point in input_data:
        sides = _get_sides(point)
        for side in sides:
            if side not in counter:
                ans += 1
            else:
                ans -= 1
            counter[side] += 1

    return ans


ans = 0


def process_input2():
    input_data = [line.split(',') for line in _read_input_file()]
    points = sorted([(int(x), int(y), int(z)) for x, y, z in input_data])

    @functools.lru_cache(None)
    def dfs3(x, y, z) -> int:
        global ans
        if x > 22 or y > 22 or z > 22 or x < 0 or y < 0 or z < 0:
            return 0
        if (x + 1, y, z) in points:
            ans += 1
        else:
            dfs3(x + 1, y, z)
        if (x, y + 1, z) in points:
            ans += 1
        else:
            dfs3(x, y + 1, z)
        if (x, y, z + 1) in points:
            ans += 1
        else:
            dfs3(x, y, z + 1)

    @functools.lru_cache(None)
    def dfs4(x, y, z) -> int:
        global ans
        if x > 22 or y > 22 or z > 22 or x < 0 or y < 0 or z < 0:
            return 0
        if (x - 1, y, z) in points:
            ans += 1
        else:
            dfs4(x - 1, y, z)
        if (x, y - 1, z) in points:
            ans += 1
        else:
            dfs4(x, y - 1, z)
        if (x, y, z - 1) in points:
            ans += 1
        else:
            dfs4(x, y, z - 1)
        return 0

    dfs3(0, 0, 0)
    dfs4(22, 22, 22)

    return ans


if __name__ == "__main__":
    print(process_input())
    print(process_input2())
