from typing import Iterator, Optional


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


mapping = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}


def _snafu_to_decimal(text: str) -> int:
    result = 0
    multiplyer = 1 / 5
    for char in reversed(text):
        multiplyer *= 5
        result += multiplyer * mapping[char]

    return int(result)


def _decimal_to_snafu(number: int, length: Optional[int] = None) -> str:

    if length == 1:
        return {i for i in mapping if mapping[i] == number}.pop()
    if not length:
        length = 1
        while number > (_snafu_to_decimal("2" * length)):
            length += 1

    if _snafu_to_decimal("1" + "2" * (length - 1)) < number:
        return f"2{_decimal_to_snafu(number - 2 * (5 ** (length - 1)), length - 1)}"

    if _snafu_to_decimal("0" + "2" * (length - 1)) < number:
        return f"1{_decimal_to_snafu(number - 1 * (5 ** (length - 1)), length - 1)}"

    if _snafu_to_decimal("-" + "2" * (length - 1)) < number:
        return f"0{_decimal_to_snafu(number + 0 * (5 ** (length - 1)), length - 1)}"

    if _snafu_to_decimal("=" + "2" * (length - 1)) < number:
        return f"-{_decimal_to_snafu(number + 1 * (5 ** (length - 1)), length - 1)}"

    return f"={_decimal_to_snafu(number + 2 * (5 ** (length - 1)), length - 1)}"


def task() -> str:
    result = 0
    for line in _read_input_file():
        num = _snafu_to_decimal(line)
        result += num

    return _decimal_to_snafu(result)


if __name__ == "__main__":
    print(task())
