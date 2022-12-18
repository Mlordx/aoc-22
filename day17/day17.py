import sys
from collections import defaultdict

movement = ''
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        movement = line.strip()

shapes = ['-', '+', 'L', 'I', 'cube']
CURRENT_SHAPE = 0
CURRENT_MOVEMENT = 0


def make_shape(floor_height):
    global CURRENT_SHAPE
    shape = shapes[CURRENT_SHAPE]
    CURRENT_SHAPE = (CURRENT_SHAPE + 1) % len(shapes)
    y = floor_height+4

    if shape == '-':
        return set([(2, y), (3, y), (4, y), (5, y)])
    if shape == '+':
        return set([(3, y), (3, y+1), (3, y+2), (2, y+1), (4, y+1)])
    if shape == 'L':
        return set([(2, y), (3, y), (4, y), (4, y+1), (4, y+2)])
    if shape == 'I':
        return set([(2, y), (2, y+1), (2, y+2), (2, y+3)])

    return set([(2, y), (3, y), (2, y+1), (3, y+1)])


def can_move(dir, tunnel, rock):
    if dir == '>':
        max_x = max([x for x, _ in rock])
        if max_x == 6:  # wall
            return False

        for point in rock:  # other rocks
            x, y = point
            if (x+1, y) in tunnel:
                return False
    elif dir == '<':
        min_x = min([x for x, _ in rock])
        if min_x == 0:
            return False

        for point in rock:
            x, y = point
            if (x-1, y) in tunnel:
                return False
    else:
        for point in rock:
            x, y = point
            if (x, y-1) in tunnel:
                return False

    return True


def draw_tunnel(tunnel):
    drawing = ''
    for y in range(50, -1, -1):
        for x in range(7):
            if (x, y) in tunnel:
                drawing += '#'
            else:
                drawing += '.'
        drawing += '\n'
    print(drawing)


def answer1():
    global CURRENT_MOVEMENT
    floor_height = -1
    tunnel = set([(x, -1) for x in range(7)])

    for _ in range(2022):
        rock = make_shape(floor_height)
        while True:
            dir = movement[CURRENT_MOVEMENT]
            if dir == '>' and can_move(dir, tunnel, rock):
                new_points = [(x+1, y) for x, y in rock]
                rock = set(new_points)

            if dir == '<' and can_move(dir, tunnel, rock):
                new_points = [(x-1, y) for x, y in rock]
                rock = set(new_points)

            CURRENT_MOVEMENT = (CURRENT_MOVEMENT + 1) % len(movement)
            if can_move('V', tunnel, rock):
                new_points = [(x, y-1) for x, y in rock]
                rock = set(new_points)
            else:
                tunnel |= rock
                floor_height = max([y for _, y in tunnel])
                break

    return max([y for _, y in tunnel]) + 1  # lowest level is 0


def snapshot(tunnel):
    max_y = max([y for _, y in tunnel])
    return frozenset([(x, max_y-y) for x, y in tunnel if max_y-y <= 50])


def answer2():
    global CURRENT_MOVEMENT, CURRENT_SHAPE
    CURRENT_MOVEMENT = 0
    CURRENT_SHAPE = 0

    floor_height = -1
    tunnel = set([(x, -1) for x in range(7)])

    target = int(1e12)
    count = 0
    known_positions = defaultdict()
    additional_rocks = 0
    jumped = False
    while count < target:
        rock = make_shape(floor_height)

        while count < target:
            dir = movement[CURRENT_MOVEMENT]

            if dir == '>' and can_move(dir, tunnel, rock):
                new_points = [(x+1, y) for x, y in rock]
                rock = set(new_points)

            if dir == '<' and can_move(dir, tunnel, rock):
                new_points = [(x-1, y) for x, y in rock]
                rock = set(new_points)

            CURRENT_MOVEMENT = (CURRENT_MOVEMENT + 1) % len(movement)
            if can_move('V', tunnel, rock):
                new_points = [(x, y-1) for x, y in rock]
                rock = set(new_points)
            else:
                tunnel |= rock
                floor_height = max([y for _, y in tunnel])
                key = (CURRENT_MOVEMENT, CURRENT_SHAPE, snapshot(tunnel))

                if key in known_positions and not jumped:
                    old_count, old_height = known_positions[key]

                    rock_count_diff = count - old_count
                    height_per_cycle = floor_height - old_height

                    repeat = (target - count) // rock_count_diff
                    additional_rocks = repeat * height_per_cycle
                    count += repeat * rock_count_diff

                known_positions[key] = (count, floor_height)

                count += 1
                break

    return max([y for _, y in tunnel]) + 1 + additional_rocks


print(answer1())
print(answer2())
