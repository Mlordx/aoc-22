import sys

paths = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
GRID = set()
MIN_X, MAX_X = 2**40, -1
MIN_Y, MAX_Y = 2**40, -1
with open(input_file, 'r') as file:
    for i, line in enumerate(file):
        paths.append([])
        stripped_line = line.strip()

        for point in stripped_line.split(' -> '):
            a, b = point.split(',')
            x, y = int(a), int(b)
            MAX_X = max(MAX_X, x)
            MIN_X = min(MIN_X, x)
            MAX_Y = max(MAX_Y, y)
            MIN_Y = min(MIN_Y, y)

            paths[i].append((x, y))


def initialize_grid():
    global GRID
    GRID = set()
    for path in paths:
        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            if x1 == x2:
                min_y = min(y1, y2)
                max_y = max(y1, y2)
                for y in range(min_y, max_y+1):
                    GRID.add((x1, y))
            else:
                min_x = min(x1, x2)
                max_x = max(x1, x2)
                for x in range(min_x, max_x+1):
                    GRID.add((x, y1))


def can_move(current_pos, part1=True):
    x, y = current_pos
    if part1:
        if y >= MAX_Y + 1:
            return None

    if (x, y+1) in GRID:
        if (x-1, y+1) in GRID:
            if (x+1, y+1) in GRID:
                return (x, y)
            else:
                return can_move((x+1, y+1), part1)
        else:
            return can_move((x-1, y+1), part1)
    else:
        return can_move((x, y+1), part1)


def answer1():
    initialize_grid()
    count = 0
    sand = (500, 0)

    while can_move(sand):
        GRID.add(can_move(sand))
        sand = (500, 0)
        count += 1

    return count


def answer2():
    initialize_grid()
    count = 0
    sand = (500, 0)

    for x in range(0, MAX_X**2):
        GRID.add((x, MAX_Y+2))

    while can_move(sand, False):
        GRID.add(can_move(sand, False))
        sand = (500, 0)
        count += 1
        if can_move(sand, False) == (500, 0):
            break

    return count + 1


print(answer1())
print(answer2())
