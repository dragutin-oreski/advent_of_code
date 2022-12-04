from typing import Iterator, Optional, Tuple
import string

mapping = {letter: idx + 1 for idx, letter in enumerate(string.ascii_letters)}


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip()


def _get_limits(line: str) -> Tuple[int, int, int, int]:
    first_elf, second_elf = line.split(',')
    first_low, first_high = first_elf.split('-')
    second_low, second_high = second_elf.split('-')
    first_low, first_high = int(first_low), int(first_high)
    second_low, second_high = int(second_low), int(second_high)

    return first_low, first_high, second_low, second_high


def _process_line(line: str) -> int:
    first_low, first_high, second_low, second_high = _get_limits(line)

    return first_low >= second_low and first_high <= second_high or \
           first_low <= second_low and first_high >= second_high


def process_input() -> int:
    return sum([_process_line(line) for line in _read_input_file()])


def _process_line2(line: str) -> int:
    first_low, first_high, second_low, second_high = _get_limits(line)

    return first_low <= second_low <= first_high or \
           first_low <= second_high <= first_high or \
           second_low <= first_low <= second_high or \
           second_low <= first_high <= second_high


def process_input2() -> int:
    return sum([_process_line2(line) for line in _read_input_file()])


if __name__ == "__main__":
    print(process_input())
    print(process_input2())
