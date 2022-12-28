import sys
from collections import defaultdict
from copy import deepcopy

GRID = set()

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for i, line in enumerate(file):
        stripped_line = line.strip()
        for j, c in enumerate(stripped_line):
            if c != '.':
                GRID.add((j, i))


def get_position(grid, directions, elf_pos, current_direction):
    x, y = elf_pos
    orthogonal_dir = directions[current_direction][0]
    possible_destination = (x + orthogonal_dir[0], y + orthogonal_dir[1])
    free = True
    for offset_x, offset_y in directions[current_direction]:
        if (x+offset_x, y+offset_y) in grid:
            free = False

    if free:
        return possible_destination

    return None


def at_least_one_surrounding_elf(grid, directions, elf_pos):
    x, y = elf_pos
    for dir in range(4):
        for offset_x, offset_y in directions[dir]:
            if (x+offset_x, y+offset_y) in grid:
                return True

    return False


def draw_grid(grid):
    min_x = min([x for x, _ in grid])
    max_x = max([x for x, _ in grid])
    min_y = min([y for _, y in grid])
    max_y = max([y for _, y in grid])

    drawing = ''
    for y in range(min_y-1, max_y+2):
        for x in range(min_x-1, max_x+2):
            if (x, y) in grid:
                drawing += '#'
            else:
                drawing += '.'

        drawing += '\n'

    print(drawing)
    print('-' * 40)


def simulate(part1=True):
    global GRID
    local_grid = deepcopy(GRID)
    directions = [
        [(0, -1), (1, -1), (-1, -1)],  # N NE NW
        [(0, 1), (1, 1), (-1, 1)],  # S SE SW
        [(-1, 0), (-1, -1), (-1, 1)],  # W NW SW
        [(1, 0), (1, -1), (1, 1)],  # E NE SE
    ]

    count = 0

    while True:
        count += 1

        if part1 and count == 11:
            break

        position_count = defaultdict(int)
        proposed_movements = defaultdict(tuple)
        for elf in local_grid:
            if not at_least_one_surrounding_elf(local_grid, directions, elf):
                continue

            for direction in range(4):
                proposed_location = get_position(local_grid, directions, elf, direction)
                if proposed_location is not None:
                    position_count[proposed_location] += 1
                    proposed_movements[elf] = proposed_location
                    break

        new_grid = set()

        for elf in local_grid:
            if elf not in proposed_movements:
                new_grid.add(elf)
            else:
                destination = proposed_movements[elf]
                if position_count[destination] < 2:
                    new_grid.add(destination)
                else:
                    new_grid.add(elf)

        if local_grid == new_grid:
            return count

        local_grid = new_grid
        directions.append(directions.pop(0))

    x = [x for x, _ in local_grid]
    y = [y for _, y in local_grid]

    return abs(max(x) - min(x) + 1) * abs(max(y) - min(y) + 1) - len(local_grid)


def answer1():
    return simulate()


def answer2():
    return simulate(False)


print(answer1())
print(answer2())
