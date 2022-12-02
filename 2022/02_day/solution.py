from typing import Iterator, Optional

SHAPE_VALUE = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}
SHAPE_TO_MY_SHAPE = {
    "A": "X",  # rock
    "B": "Y",  # paper
    "C": "Z",  # scissors
}
SHAPES = ["A", "C", "B"]


def _read_input_file(path: str = 'input.txt') -> Iterator[Optional[str]]:
    with open(path) as file:
        for line in file:
            yield line.strip()


def _get_outcome_value(shape1: str, shape2: str) -> int:
    shape1 = SHAPE_TO_MY_SHAPE[shape1]
    if shape1 == shape2:
        return 3

    if (shape1 == "X" and shape2 == "Z") or \
        (shape1 == "Y" and shape2 == "X") or \
        (shape1 == "Z" and shape2 == "Y"):
        return 0
    return 6


def _get_play_sum(shape1: str, shape2: str) -> int:
    return SHAPE_VALUE[shape2] + _get_outcome_value(shape1=shape1, shape2=shape2)


def get_total_score1():
    return sum([_get_play_sum(*line.split()) for line in _read_input_file()])


def _decide_my_shape(shape1: str, shape2: str) -> str:
    if shape2 == "Y":
        return SHAPE_TO_MY_SHAPE[shape1]

    idx = SHAPES.index(shape1)
    if shape2 == "X":
        my_idx = (idx + 1) % 3
    else:
        my_idx = (idx - 1) % 3

    return SHAPE_TO_MY_SHAPE[SHAPES[my_idx]]


def _get_outcome_value2(shape2: str) -> int:
    if shape2 == "X":
        return 0
    if shape2 == "Y":
        return 3
    return 6


def _get_play_sum2(shape1: str, shape2: str) -> int:
    my_shape = _decide_my_shape(shape1, shape2)
    return SHAPE_VALUE[my_shape] + _get_outcome_value2(shape2=shape2)


def get_total_score2():
    return sum([_get_play_sum2(*line.split()) for line in _read_input_file()])


if __name__ == "__main__":
    print(get_total_score1())
    print(get_total_score2())
