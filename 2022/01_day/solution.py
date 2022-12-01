from typing import Iterator, Optional


def _read_input_file(path: str = 'input.txt') -> Iterator[Optional[str]]:
    with open(path) as file:
        for line in file:
            yield line.strip()


def _get_calories_per_elf() -> Iterator[int]:
    calories = 0
    for line in _read_input_file():
        if not line:
            yield calories
            calories = 0
        else:
            calories += int(line)


def get_most_calories() -> int:
    high = 0
    for line in _get_calories_per_elf():
        if line > high:
            high = line
    return high


def get_most_three_calories() -> int:
    calories = [0, 0, 0]
    low = 0
    for line in _get_calories_per_elf():
        if line > low:
            calories.remove(low)
            calories.append(line)
            low = min(calories)
    return sum(calories)


if __name__ == "__main__":
    print(get_most_calories())
    print(get_most_three_calories())
