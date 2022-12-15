from typing import Iterator, Optional, List
import re

REG = "Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)"


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _read_line():
    for line in _read_input_file():
        yield [int(elem) for elem in re.search(REG, line).groups()]


def _get_limits():
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    min_beacon_x = None
    max_beacon_x = None
    min_beacon_y = None
    max_beacon_y = None
    max_dist = 0
    for sensor_x, sensor_y, beacon_x, beacon_y in _read_line():
        if not min_x:
            min_x = sensor_x
        if not max_x:
            max_x = sensor_x
        if not max_y:
            max_y = sensor_y
        if not min_y:
            min_y = sensor_y
        if not min_beacon_x:
            min_beacon_x = sensor_x
        if not max_beacon_x:
            max_beacon_x = sensor_x
        if not max_beacon_y:
            max_beacon_y = sensor_y
        if not min_beacon_y:
            min_beacon_y = sensor_y

        if sensor_x < min_x:
            min_x = sensor_x
        if sensor_x > max_x:
            max_x = sensor_x
        if beacon_x < min_beacon_x:
            min_beacon_x = beacon_x
        if beacon_x > max_beacon_x:
            max_beacon_x = beacon_x

        if beacon_y > max_beacon_y:
            max_beacon_y = beacon_y
        if sensor_y > max_y:
            max_y = sensor_y
        if beacon_y < min_beacon_y:
            min_beacon_y = beacon_y
        if sensor_y < min_y:
            min_y = sensor_y

        dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        if dist > max_dist:
            max_dist = dist

    return min(min_x - max_dist, min_beacon_x), max(max_x + max_dist, max_beacon_x), \
           min(min_y - max_dist, min_beacon_y, 0), max(max_y + max_dist, max_beacon_y), max_dist


def _add_to_row_n(amount: int, row_n: List, x: int):
    if amount <= 0:
        return row_n

    if row_n[x] == '..':
        row_n[x] = '##'
    amount -= 1

    around_central = 0
    while amount:
        around_central += 1
        if row_n[x + around_central] == '..':
            row_n[x + around_central] = '##'
        if row_n[x - around_central] == '..':
            row_n[x - around_central] = '##'

        amount -= 1

    return row_n


def take_two(n) -> int:
    min_x, max_x, min_y, max_y, max_dist = _get_limits()
    shift = abs(min_x)
    width = (abs(min_x) + abs(max_x) + 1)
    row_n = ['..'] * width

    for sensor_x, sensor_y, beacon_x, beacon_y in _read_line():
        dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        x = sensor_x + shift
        if sensor_y == n:
            row_n[x] = "S"
        if beacon_y == n:
            row_n[beacon_x + shift] = "B"
        amount_in_row_n = dist - abs(sensor_y - n) + 1
        row_n = _add_to_row_n(amount=amount_in_row_n, row_n=row_n, x=x)

    return sum([row_n.count("##")])


def _get_all_sensors_and_distances():
    result = []
    for sensor_x, sensor_y, beacon_x, beacon_y in _read_line():
        dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        result.append((sensor_x, sensor_y, dist))
    return result


def _dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def _walk_around(x_original, y_original, dist, limit):

    x = x_original + dist + 1
    y = y_original

    while x > x_original:
        if 0 <= x <= limit and 0 <= y <= limit:
            yield x, y
        x -= 1
        y -= 1
    while y_original > y:
        if 0 <= x <= limit and 0 <= y <= limit:
            yield x, y
        x -= 1
        y += 1
    while x_original > x:
        if 0 <= x <= limit and 0 <= y <= limit:
            yield x, y
        x += 1
        y += 1
    while y > y_original:
        if 0 <= x <= limit and 0 <= y <= limit:
            yield x, y
        x += 1
        y -= 1


def part_two_take_three(limit):
    all_sensors_and_distances = _get_all_sensors_and_distances()
    for x, y, dist in all_sensors_and_distances:
        for x_cand, y_cand in _walk_around(x, y, dist, limit):
            is_somewhere = False
            for _x, _y, _d in all_sensors_and_distances:
                if _dist(x_cand, y_cand, _x, _y) <= _d:
                    is_somewhere = True
                    break

            if not is_somewhere:
                return x_cand, y_cand, x_cand * 4_000_000 + y_cand


if __name__ == "__main__":
    print(take_two(2000000))
    print(part_two_take_three(4000000))
