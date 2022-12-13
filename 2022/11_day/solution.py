from typing import Iterator, Optional, List


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def read_monkeys():
    reader = _read_input_file()
    line = next(reader)
    while line:
        idx = int(line.split()[-1].strip(":"))
        line = next(reader)
        starting_items = [int(item.strip()) for item in line.split(":")[1].split(",")]
        line = next(reader)
        operation = line.split("new = ")[-1].strip()
        line = next(reader)
        test = int(line.split()[-1])
        line = next(reader)
        test_true = int(line.split()[-1])
        line = next(reader)
        test_false = int(line.split()[-1])
        line = next(reader, None)
        line = next(reader, None)

        monkey = Monkey(
            idx=idx,
            starting_items=starting_items,
            operation=operation,
            test=test,
            test_true=test_true,
            test_false=test_false,
        )
        MONKEYS.append(monkey)

    return MONKEYS


def run_rounds(cycles: Optional[int] = 20, divide_by_three=True):
    MONKEYS = read_monkeys()
    idx = 0
    for _ in tqdm(range(cycles)):
        for monkey in MONKEYS:
            monkey.inspect(divide_by_three=divide_by_three)
        idx += 1
        if idx == 1 or idx == 20 or idx % 1000 == 0:
            for monkey in MONKEYS:
                print(monkey.idx, monkey.inspections)

    sorted_monkeys = sorted(MONKEYS, key=lambda monkey: monkey.inspections, reverse=True)

    for monkey in sorted_monkeys:
        print(monkey)

    return sorted_monkeys[0].inspections * sorted_monkeys[1].inspections


def multiply(num1: int, num2: int) -> int:
    num1 = str(num1)
    num2 = str(num2)

    def multiply_one(num1: str, num2: str) -> str:
        num2 = int(num2)
        over = 0
        result = ''
        for char in reversed(num1):
            mul = str(num2 * int(char))
            if over:
                mul = str(int(mul) + over)

            if len(mul) == 2:
                over = int(mul[0])
                mul = mul[1]
            else:
                over = 0

            result1 = f"{mul}{result}"
            result = result1

        if over:
            result = f"{over}{result}"

        return result

    ans = []
    for char in num2:
        ans.append(multiply_one(num1, char))

    def add_two(num1: str, num2: str, num_of_nulls: int) -> str:
        nulls = num_of_nulls * "0"
        num1 = f"{num1}{nulls}"
        ans = ''
        over = 0
        for idx in range(1, max(len(num1), len(num2)) + 1):
            digit1 = int(num1[-idx]) if idx <= len(num1) else 0
            digit2 = int(num2[-idx]) if idx <= len(num2) else 0
            res = str(sum([over, digit1, digit2]))

            if len(res) == 2:
                over = int(res[0])
                res = res[1]
            else:
                over = 0

            ans1 = f"{res}{ans}"
            ans = ans1

        if over:
            ans = f"{over}{ans}"

        return ans

    total_sum = ''
    for idx, elem in enumerate(reversed(ans)):
        total_sum1 = add_two(elem, total_sum, idx)
        # print(elem, total_sum, total_sum1)
        total_sum = total_sum1

    total_sum = total_sum.lstrip("0") or "0"
    return int(total_sum)


if __name__ == "__main__":
    # print(run_rounds())
    print(run_rounds(cycles=10_000, divide_by_three=False))
