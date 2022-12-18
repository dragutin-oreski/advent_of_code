import functools
from copy import deepcopy
from typing import Iterator, Optional, List, Tuple

objects = [
    [
        [" ", " ", "#", "#", "#", "#", " "],
    ],
    [
        [" ", " ", " ", "#", " ", " ", " "],
        [" ", " ", "#", "#", "#", " ", " "],
        [" ", " ", " ", "#", " ", " ", " "],
    ],
    [
        [" ", " ", " ", " ", "#", " ", " "],
        [" ", " ", " ", " ", "#", " ", " "],
        [" ", " ", "#", "#", "#", " ", " "],
    ],
    [
        [" ", " ", "#", " ", " ", " ", " "],
        [" ", " ", "#", " ", " ", " ", " "],
        [" ", " ", "#", " ", " ", " ", " "],
        [" ", " ", "#", " ", " ", " ", " "],
    ],
    [
        [" ", " ", "#", "#", " ", " ", " "],
        [" ", " ", "#", "#", " ", " ", " "],
    ],
]
empty_line = [" ", " ", " ", " ", " ", " ", " "]
lower_bound = [
    [0, 1, 2, 3],
    [1, 3, 4],
    [2, 3, 4],
    [3],
    [2, 3],
]
right_bound = [
    [3],
    [0, 3, 4],
    [0, 1, 4],
    [0, 1, 2, 3],
    [1, 3],
]
left_bound = [
    [0],
    [0, 1, 4],
    [0, 1, 2],
    [0, 1, 2, 3],
    [0, 2],
]


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _get_direction() -> List[str]:
    return [direction for direction in next(_read_input_file())]


def _clean_tower(tower) -> List[str]:
    while True:
        if tower[0] == empty_line:
            del tower[0]
        else:
            break
    return tower


def _add_new_object(obj, tower):
    tower.insert(0, deepcopy(empty_line))
    tower.insert(0, deepcopy(empty_line))
    tower.insert(0, deepcopy(empty_line))
    for line in reversed(obj):
        tower.insert(0, deepcopy(line))

    return tower


@functools.lru_cache(5)
def _get_positions(idx: int) -> List[Tuple[int, int]]:
    obj = objects[idx]
    positions = []
    for m in range(len(obj)):
        for n in range(len(obj[0])):
            if obj[m][n] == "#":
                positions.append((m, n))

    return positions


def _can_drop(tower: List[List[str]], positions: List[Tuple[int, int]], idx: int) -> bool:

    for elem in lower_bound[idx]:
        point_m, point_n = positions[elem]
        if (point_m + 1) == len(tower) or tower[point_m + 1][point_n] == "#":
            return False

    return True


def _can_move(tower: List[List[str]], positions: List[Tuple[int, int]], direction: str, idx: int) -> bool:
    if direction == ">":
        for elem in right_bound[idx]:
            point_m, point_n = positions[elem]
            if (point_n + 1) > 6 or tower[point_m][point_n + 1] == "#":
                return False
        return True

    for elem in left_bound[idx]:
        point_m, point_n = positions[elem]
        if (point_n - 1) < 0 or tower[point_m][point_n - 1] == "#":
            return False
    return True


def _move(tower: List[List[str]], positions: List[Tuple[int, int]], direction: str) -> List[Tuple[int, int]]:
    new_positions = []
    if direction == ">":
        for point_m, point_n in positions:
            tower[point_m][point_n] = " "
            new_positions.append((point_m, point_n + 1))

    elif direction == "<":
        for point_m, point_n in positions:
            tower[point_m][point_n] = " "
            new_positions.append((point_m, point_n - 1))

    elif direction == "v":
        for point_m, point_n in positions:
            tower[point_m][point_n] = " "
            new_positions.append((point_m + 1, point_n))

    for point_m, point_n in new_positions:
        tower[point_m][point_n] = "#"

    return new_positions


def tetris(num_of_rocks):
    directions = _get_direction()
    len_directions = len(directions)

    tower = []
    ans = 0
    idx_direction = 0
    past_idx = 0
    prev_height = 0
    for idx in range(num_of_rocks):
        obj = deepcopy(objects[idx % len(objects)])

        positions = _get_positions(idx % len(objects))
        tower = _add_new_object(obj=obj, tower=tower)
        while True:
            direction = directions[idx_direction % len_directions]
            idx_direction += 1

            if _can_move(tower=tower, direction=direction, positions=positions, idx=idx % len(objects)):
                positions = _move(tower=tower, direction=direction, positions=positions)

            if _can_drop(tower=tower, positions=positions, idx=idx % len(objects)):
                positions = _move(tower=tower, positions=positions, direction="v")
            else:
                tower = _clean_tower(tower)
                break

        # after noticing the repeating pattern, use these values to calculate the result
        if (idx + 1) in (86 * 5, 87 * 5, 408 * 5, 429 * 5, 86 * 5 + 660):
            print(len(tower))

        # use this part of the code to detect the repeating pattern
        if (idx + 1) % 5 == 0:
            # print(len(tower) - prev_height)
            past_idx = idx_direction
            prev_height = len(tower)

    return ans + len(tower)


if __name__ == "__main__":
    print(tetris(2022))
    tetris(20022)
    # num = 1_000_000_000_000
    # 1031 + height_at_86_5 + ((num) // (342 * 5)) * 2620 = 1_532_163_742_758
