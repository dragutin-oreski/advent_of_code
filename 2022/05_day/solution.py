from typing import Iterator, Optional, List
import string
import re

mapping = {letter: idx + 1 for idx, letter in enumerate(string.ascii_letters)}


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _get_buckets(reader) -> List[List[str]]:
    buckets = []

    for line in reader:
        if not line.strip():
            break

        if not buckets:
            num = int((len(line) + 1) / 4)
            buckets = [[] for _ in range(num + 1)]

        idx = 0
        while line:
            idx += 1
            part = line[:4]
            if not part:
                if len(line) < 4:
                    line = ''
                else:
                    line = line[4:]
                continue

            letter = part[1].strip()
            if len(line) < 4:
                line = ''
            else:
                line = line[4:]
            if letter:
                buckets[idx].append(letter)

    old_buckets = buckets
    buckets = [[] for _ in range(len(old_buckets))]
    for bucket in old_buckets:
        if not bucket:
            continue
        idx = None
        for elem in reversed(bucket):
            if not elem:
                continue
            if not idx:
                idx = int(elem)
                continue
            buckets[idx].append(elem)

    return buckets


def process_line() -> str:
    reader = _read_input_file()
    buckets = _get_buckets(reader)

    for line in reader:
        match = re.search(r"move (\d*) from (\d*) to (\d*)", line)
        num, origin, dest = match.groups()
        num, origin, dest = int(num), int(origin), int(dest)
        for _ in range(num):
            elem = buckets[origin].pop()
            buckets[dest].append(elem)

    for bucket in buckets:
        print(bucket)

    ans = ''
    for idx in range(1, len(buckets)):
        ans = f"{ans}{buckets[idx].pop() if buckets[idx] else ''}"

    return ans


def process_line2() -> str:
    reader = _read_input_file()
    buckets = _get_buckets(reader)

    for line in reader:
        match = re.search(r"move (\d*) from (\d*) to (\d*)", line)
        num, origin, dest = match.groups()
        num, origin, dest = int(num), int(origin), int(dest)

        elems = [buckets[origin].pop() for _ in range(num)]
        buckets[dest] = [*buckets[dest], *reversed(elems)]

    for bucket in buckets:
        print(bucket)

    ans = ''
    for idx in range(1, len(buckets)):
        ans = f"{ans}{buckets[idx].pop() if buckets[idx] else ''}"

    return ans


if __name__ == "__main__":
    print(process_line())
    print(process_line2())
