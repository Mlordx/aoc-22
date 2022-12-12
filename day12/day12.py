import sys
from collections import defaultdict
import math

GRID = defaultdict()
starting_position = (0, 0)
starting_positions = []

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for i, line in enumerate(file):
        stripped_line = line.strip()
        for j, c in enumerate(stripped_line):
            GRID[(i, j)] = c
            if c == 'S':
                starting_position = (i, j)
            if c == 'a':
                starting_positions.append((i, j))


def can_jump(current, target):
    if target not in GRID:
        return False

    current_value = ord('a') if GRID[current] == 'S' else ord(GRID[current])
    target_value = ord('z') if GRID[target] == 'E' else ord(GRID[target])

    if target_value - current_value == 1:
        return True

    if target_value - current_value <= 0:
        return True

    return False


def bfs(starting_position):
    queue = [(starting_position, 0)]
    visited = set()

    while len(queue) > 0:
        current, distance = queue.pop(0)
        x, y = current

        if current in visited:
            continue

        visited.add(current)

        if GRID[current] == 'E':
            return distance

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            off_x, off_y = direction
            target = (x+off_x, y+off_y)

            if can_jump(current, target):
                queue.append((target, distance + 1))

    return math.inf


def answer1():
    return bfs(starting_position)


def answer2():
    resp = math.inf
    for starting_pos in starting_positions:
        resp = min(resp, bfs(starting_pos))

    return resp


print(answer1())
print(answer2())
