import functools
from typing import Iterator, Optional, List, Union


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _read_pairs():
    reader = _read_input_file()
    while True:
        first = next(reader, None)
        second = next(reader, None)
        if not first:
            break
        yield first, second
        next(reader, None)


def _compare_values(one: Union[List, int], two: Union[List, int]) -> Union[int, bool]:
    if isinstance(one, int) and isinstance(two, int):
        if one == two:
            return 1
        if one < two:
            return True
        if one > two:
            return False

    if not isinstance(one, list):
        one = [one]
    if not isinstance(two, list):
        two = [two]

    for elem1, elem2 in zip(one, two):
        value = _compare_values(elem1, elem2)
        if isinstance(value, bool):
            return value

    if len(one) == len(two):
        return 1

    if len(one) < len(two):
        return True

    return False


def _is_in_right_order(first: Union[List, int], second: Union[List, int]) -> bool:

    if not isinstance(first, list):
        first = [first]
    if not isinstance(second, list):
        second = [second]

    for f, s in zip(first, second):
        value = _compare_values(f, s)
        if isinstance(value, bool):
            return value

    return len(first) <= len(second)


def sum_right_order_indices():
    ans = 0
    for idx, (first, second) in enumerate(_read_pairs()):
        if _is_in_right_order(eval(first), eval(second)):
            ans += idx + 1

    return ans


def _compare(first: Union[List, int], second: Union[List, int]) -> int:
    if _is_in_right_order(first, second):
        return -1
    return 1


def put_in_the_right_order() -> int:
    all_inputs = [eval(row) for row in _read_input_file() if row]
    package_0 = [[2]]
    package_1 = [[6]]
    all_inputs.append(package_0)
    all_inputs.append(package_1)

    sorted_inputs = sorted(all_inputs, key=functools.cmp_to_key(_compare))

    return (sorted_inputs.index(package_0) + 1) * (sorted_inputs.index(package_1) + 1)


if __name__ == "__main__":
    print(sum_right_order_indices())
    print(put_in_the_right_order())
