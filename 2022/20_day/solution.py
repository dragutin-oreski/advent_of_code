from typing import Iterator, Optional, Dict

from tqdm import tqdm


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


class Node:
    def __init__(self, val, next: Optional["Node"] = None, previous: Optional["Node"] = None) -> "Node":
        self.val = val
        self.next = next
        self.previous = previous

    def __repr__(self) -> str:
        return str(self.val)


def _get_linked_list(multiply: Optional[int] = 1) -> Dict[int, Node]:
    previous_node = None
    all_nodes = {}
    for idx, num in enumerate(_read_input_file()):
        node = Node(
            val=int(num) * multiply,
            next=None,
            previous=previous_node
        )
        all_nodes[idx] = node
        if previous_node:
            previous_node.next = node
        previous_node = node

    last_node = list(all_nodes.values())[-1]
    first_node = list(all_nodes.values())[0]

    last_node.next = first_node
    first_node.previous = last_node

    return all_nodes


def task2(multiply: Optional[int] = 1, rounds: Optional[int] = 1):
    nodes = _get_linked_list(multiply=multiply)
    len_nodes = len(nodes)

    for i in range(rounds):
        for node in tqdm(nodes.values()):
            value = node.val % (len_nodes - 1)
            if value == 0:
                continue
            if value > 0:
                while value:
                    prev_node = node.previous
                    next_node = node.next

                    prev_node.next = next_node
                    next_node.previous = prev_node

                    node.previous = next_node
                    node.next = next_node.next
                    next_node.next = node
                    node.next.previous = node
                    value -= 1
            else:
                while value < 0:
                    prev_node = node.previous
                    next_node = node.next

                    prev_node.next = next_node
                    next_node.previous = prev_node

                    node.previous = prev_node.previous
                    node.next = prev_node
                    prev_node.previous = node
                    node.previous.next = node
                    value += 1

    head = nodes[0]
    while head.val != 0:
        head = head.next

    total = []
    for idx in [1000, 2000, 3000]:
        idx = idx % len(nodes)
        node = head
        while idx:
            node = node.next
            idx -= 1
        total.append(node.val)
        print(node.val)

    return sum(total)


if __name__ == "__main__":
    print(task2())
    print(task2(multiply=811589153, rounds=10))
