from typing import Iterator, Optional


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def process_input():
    ans = {(20 + 40 * i): None for i in range(6)}
    X = 1
    cycle = 1
    for line in _read_input_file():
        if cycle in ans:
            ans[cycle] = X

        if 'noop' in line:
            cycle += 1
            continue

        value = int(line.split()[1])
        cycle += 1
        if cycle in ans:
            ans[cycle] = X

        cycle += 1
        X += value

    print(ans)

    return sum([k * v for k, v in ans.items()])


def _get_char(X: int, cycle: int) -> str:
    if X <= (cycle % 40) <= (X + 2):
        return "#"
    return " "


def process_input2():
    ans = ''
    X = 1
    cycle = 1
    for line in _read_input_file():
        ans = f"{ans}{_get_char(X, cycle)}"

        if 'noop' in line:
            cycle += 1
            continue

        value = int(line.split()[1])
        cycle += 1
        ans = f"{ans}{_get_char(X, cycle)}"

        cycle += 1
        X += value

    img = [ans[i:i + 40] for i in range(0, len(ans), 40)]
    for line in img:
        print(line)


if __name__ == "__main__":
    print(process_input())
    process_input2()
