from typing import Iterator, Optional
import string

mapping = {letter: idx + 1 for idx, letter in enumerate(string.ascii_letters)}


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip()


def _process_line(line: str) -> int:
    middle = int(len(line)/2)
    first = set(line[:middle])
    second = set(line[middle:])

    res = first.intersection(second).pop()

    return mapping[res]


def process_input() -> int:
    return sum([_process_line(line) for line in _read_input_file()])


def _read_groups() -> Iterator[str]:

    items = []
    for line in _read_input_file():
        items.append(line)

        if len(items) == 3:
            yield items
            items = []


def process_group() -> int:
    ans = 0
    for item1, item2, item3 in _read_groups():
        s1 = set(item1)
        s2 = set(item2)
        s3 = set(item3)

        result = s1.intersection(s2).intersection(s3).pop()
        ans += mapping[result]

    return ans


if __name__ == "__main__":
    print(process_input())
    print(process_group())
