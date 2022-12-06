from typing import Iterator, Optional, List
import string
import re

mapping = {letter: idx + 1 for idx, letter in enumerate(string.ascii_letters)}


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _find_start(line: str, n: int) -> int:
    for idx in range(n - 2, len(line)):
        word = line[idx - (n - 1): idx + 1]
        if len(set(word)) == n:
            print(idx, word, line[idx])
            return idx + 1


def process_line() -> int:

    for line in _read_input_file():
        return _find_start(line, n=4)


def process_line2() -> int:

    for line in _read_input_file():
        return _find_start(line, n=14)


if __name__ == "__main__":
    print(process_line())
    print(process_line2())
