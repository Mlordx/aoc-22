import sys
from copy import deepcopy

GRID = set()
blizzards = {
    '>': [],
    '<': [],
    'v': [],
    '^': [],
}
STARTING_POSITION = None
TARGET = None
MAX_X = -1
MAX_Y = -1

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for i, line in enumerate(file):
        MAX_Y = i - 1
        stripped_line = line.strip()
        for j, c in enumerate(stripped_line):
            MAX_X = j - 1
            if c != '#':
                GRID.add((j, i))

                if STARTING_POSITION is None:
                    STARTING_POSITION = (j, i)

                TARGET = (j, i)
            if c in blizzards.keys():
                blizzards[c].append((j, i))


def move_blizzards(blizzards):
    new_blizzards = []
    for blizz in blizzards['>']:
        x, y = blizz
        new_blizzards.append((x+1, y) if x < MAX_X else (1, y))

    blizzards['>'] = new_blizzards

    new_blizzards = []
    for blizz in blizzards['<']:
        x, y = blizz
        new_blizzards.append((x-1, y) if x > 1 else (MAX_X, y))

    blizzards['<'] = new_blizzards

    new_blizzards = []
    for blizz in blizzards['v']:
        x, y = blizz
        new_blizzards.append((x, y+1) if y < MAX_Y else (x, 1))

    blizzards['v'] = new_blizzards

    new_blizzards = []
    for blizz in blizzards['^']:
        x, y = blizz
        new_blizzards.append((x, y-1) if y > 1 else (x, MAX_Y))

    blizzards['^'] = new_blizzards

    return blizzards


def blizzards_given_time(blizzards, time):
    new_blizzards = deepcopy(blizzards)
    for _ in range(time):
        new_blizzards = move_blizzards(new_blizzards)

    points = []
    for direction in new_blizzards:
        for p in new_blizzards[direction]:
            points.append(p)

    return set(points)


def bfs(grid, blizzards, start, target, starting_time):
    queue = [(start, starting_time)]
    seen = set()
    while queue:
        position, time = queue.pop(0)
        x, y = position

        if position == target:
            return time

        if (position, time) in seen:
            continue

        seen.add((position, time))

        adjs = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]

        for adj in adjs:
            off_x, off_y = adj

            if (x+off_x, y+off_y) in grid and \
               (x+off_x, y+off_y) not in blizzards[(time+1) % 300]:
                queue.append(((x+off_x, y+off_y), time+1))


def answer1():
    new_blizzards = []
    for i in range(301):
        new_blizzards.append(blizzards_given_time(blizzards, i))

    return bfs(GRID, new_blizzards, STARTING_POSITION, TARGET, 0)


def answer2():
    new_blizzards = []
    for i in range(301):
        new_blizzards.append(blizzards_given_time(blizzards, i))

    t1 = bfs(GRID, new_blizzards, STARTING_POSITION, TARGET, 0)
    t2 = bfs(GRID, new_blizzards, TARGET, STARTING_POSITION, t1)
    t3 = bfs(GRID, new_blizzards, STARTING_POSITION, TARGET, t2)

    return t3


print(answer1())
print(answer2())
