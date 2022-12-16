import sys
from collections import defaultdict

nearest_beacon = defaultdict()
known_positions = set()
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        stripped_line = line.strip()
        p1, p2 = stripped_line.split('|')
        x1, y1 = p1.split(',')
        x1, y1 = int(x1), int(y1)

        x2, y2 = p2.split(',')
        x2, y2 = int(x2), int(y2)

        nearest_beacon[(x1, y1)] = (x2, y2)
        known_positions.add((x1, y1))
        known_positions.add((x2, y2))


def manhanttan_dist(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1-x2) + abs(y1-y2)


def impossible_locations_by_height(height, sensor, beacon):
    impossible = set()

    x1, y1 = sensor

    dist = manhanttan_dist(sensor, beacon)

    if abs(height - y1) > dist:
        return set()

    off_y = abs(height - y1)
    off_x = dist - off_y
    impossible.add((x1 - off_x, x1 + off_x))
    return impossible


def contains(interval, value):
    a, b = interval
    return a <= value <= b


def mark_possible_positions(height, sensor, beacon):
    possible_positions = set()
    x1, y1 = sensor
    dist = manhanttan_dist(sensor, beacon)
    for off_x in range(-dist-1, dist+2):
        plus_y = abs(dist+1 - abs(off_x))
        minus_y = -plus_y

        new_x = x1 + off_x
        if new_x < 0 or new_x > 2*height:
            continue
        for off_y in [plus_y, minus_y]:
            new_y = y1 + off_y
            if new_y < 0 or new_y > 2*height:
                continue

            possible_positions.add((new_x, new_y))

    for possible_position in possible_positions:
        x, y = possible_position
        answer = True

        for other_sensor in nearest_beacon:
            if other_sensor == sensor:
                continue

            impossible = impossible_locations_by_height(
                y,
                other_sensor,
                nearest_beacon[other_sensor]
            )

            for interval in impossible:
                if contains(interval, x):
                    answer = False
                    break

        if answer:
            return (x, y)

    return None


def answer1():
    IMPOSSIBLE_POSITIONS = set()
    for sensor in nearest_beacon:
        IMPOSSIBLE_POSITIONS.update(
            impossible_locations_by_height(2000000, sensor, nearest_beacon[sensor])
        )

    marked = set()
    for x1, x2 in IMPOSSIBLE_POSITIONS:
        x1, x2 = min(x1, x2), max(x1, x2)
        for i in range(x1, x2+1):
            if (i, 2000000) in known_positions:
                continue
            marked.add(i)

    return len(marked)


def answer2():
    for sensor in nearest_beacon:
        answer = mark_possible_positions(2000000, sensor, nearest_beacon[sensor])
        if answer is not None:
            return answer[0] * 4000000 + answer[1]


print(answer1())
print(answer2())
