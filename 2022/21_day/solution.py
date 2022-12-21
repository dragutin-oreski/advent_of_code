from typing import Iterator, Optional


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n').split(":")


class Monkey:
    def __init__(self, val: Optional[int] = None, name: Optional[str] = None, formula: Optional[str] = None) -> "Monkey":
        self.val = val
        self.name = name
        self.formula = formula
        self.depends_on_1 = ""
        self.depends_on_2 = ""
        self.operation = ""

    def __repr__(self) -> str:
        return str(f"name: {self.name}, val: {self.val}, formula: {self.formula}, depends_on_1: {self.depends_on_1}, depends_on_2: {self.depends_on_2}, operation: {self.operation},")

    def calc_val(self) -> int:
        if self.val:
            return self.val

        one = monkeys[self.depends_on_1]
        two = monkeys[self.depends_on_2]

        return int(eval(f"{one.calc_val()} {self.operation} {two.calc_val()}"))

    def ensure_val(self, needed_val = None) -> int:
        if not self.val and not self.depends_on_1:
            raise ValueError(f'yell number {needed_val}')

        monkey_one = monkeys[self.depends_on_1]
        monkey_two = monkeys[self.depends_on_2]

        try:
            monkey_one_val = monkey_one.calc_val()
        except KeyError:
            monkey_two_val = monkey_two.calc_val()
            if self.operation == '==':
                _needed_val = monkey_two_val
            elif self.operation == '+':
                _needed_val = needed_val - monkey_two_val
            elif self.operation == '-':
                _needed_val = needed_val + monkey_two_val
            elif self.operation == '*':
                _needed_val = int(needed_val / monkey_two_val)
            elif self.operation == '/':
                _needed_val = int(needed_val * monkey_two_val)
            monkey_one.ensure_val(_needed_val)

        try:
            monkey_two_val = monkey_two.calc_val()
        except KeyError:
            monkey_one_val = monkey_one.calc_val()
            if self.operation == '==':
                _needed_val = monkey_one_val
            elif self.operation == "+":
                _needed_val = needed_val - monkey_one_val
            elif self.operation == "-":
                _needed_val = monkey_one_val - needed_val
            elif self.operation == "*":
                _needed_val = int(needed_val / monkey_one_val)
            elif self.operation == "/":
                _needed_val = int(monkey_one_val / needed_val)
            monkey_two.ensure_val(_needed_val)


monkeys = {}
for monkey_name, value in _read_input_file():
    monkey = Monkey(name=monkey_name.strip())
    value = value.strip()
    if value.isnumeric():
        monkey.val = int(value)
    else:
        value_split = value.split()
        monkey.formula = value
        monkey.depends_on_1 = value_split[0].strip()
        monkey.depends_on_2 = value_split[-1].strip()
        monkey.operation = value_split[1].strip()

    monkeys[monkey_name] = monkey


def task1():
    return monkeys['root'].calc_val()


def task2():
    monkeys['root'].operation = '=='
    monkeys['humn'].val = None

    monkeys['root'].ensure_val()


if __name__ == "__main__":
    print(task1())
    print(task2())
