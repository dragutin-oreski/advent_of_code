from typing import Iterator, Optional, Set, Tuple, List

mask = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]


def _read_input_file(path: Optional[str] = 'input.txt') -> Iterator[str]:
    with open(path) as file:
        for line in file:
            yield line.strip('\n')


def _get_points():
    input_data = [line.split(',') for line in _read_input_file()]
    return set(sorted([(int(x), int(y), int(z)) for x, y, z in input_data]))


def calc_not_shared_surface_area(points: Set[Tuple[int, int, int]]) -> int:
    ans = 0

    for x, y, z in points:
        ans += 6
        for dx, dy, dz in mask:
            if (x + dx, y + dy, z + dz) in points:
                ans -= 1

    return ans


def _get_air_pockets() -> List[Set[Tuple[int, int, int]]]:
    active_points = _get_points()
    all_points = {(x, y, z) for x in range(20) for y in range(20) for z in range(20)}
    empty_points = list(all_points - active_points)
    air_pockets = []

    while empty_points:
        points_to_check = [empty_points[0]]
        current_air_pocket = set()

        while len(points_to_check):
            point = points_to_check.pop()

            if point in empty_points:
                current_air_pocket.add(point)
                empty_points.remove(point)

                x, y, z = point
                for dx, dy, dz in mask:
                    points_to_check.append((x + dx, y + dy, z + dz))

        if (0, 0, 0) not in current_air_pocket:
            air_pockets.append(current_air_pocket)

    return air_pockets


def calc_outer_surface_area() -> int:
    active_points = _get_points()
    air_pockets = _get_air_pockets()

    return calc_not_shared_surface_area(active_points) -\
           sum([calc_not_shared_surface_area(air_pocket) for air_pocket in air_pockets])


if __name__ == "__main__":
    print(calc_not_shared_surface_area(_get_points()))
    print(calc_outer_surface_area())
