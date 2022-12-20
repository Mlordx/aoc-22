import sys

cubes = set()
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for unstripped_line in file:
        line = unstripped_line.strip().split(',')
        x, y, z = line
        x, y, z = int(x), int(y), int(z)
        cubes.add((x, y, z))


def adjacent(cube1, cube2):
    x1, y1, z1 = cube1
    x2, y2, z2 = cube2

    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2) == 1


def surface_area(lava):
    total = 0
    scanned_lava = set()

    for cube in lava:
        adjacents = 0
        for scanned in scanned_lava:
            adjacents += 1 if adjacent(scanned, cube) else 0

        total += 6 - 2 * adjacents
        scanned_lava.add(cube)

    return total


def answer1():
    return surface_area(cubes)


def mark_outside(min_x, max_x, min_y, max_y, min_z, max_z):
    queue = [(min_x, min_y, min_z)]
    visited = set()
    count = 0

    def inside_bounding_box(x, y, z):
        return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z

    while queue:
        x, y, z = queue.pop(0)
        if (x, y, z) in visited:
            continue

        visited.add((x, y, z))
        count += 1

        offsets = [(+1, 0, 0), (-1, 0, 0), (0, +1, 0), (0, -1, 0), (0, 0, +1), (0, 0, -1)]

        for offset in offsets:
            off_x, off_y, off_z = offset
            adj = (x+off_x, y+off_y, z+off_z)
            if adj not in cubes and inside_bounding_box(*adj):
                queue.append(adj)

    return visited


def answer2():
    min_x, max_x = 2**32, -1
    min_y, max_y = 2**32, -1
    min_z, max_z = 2**32, -1

    for x, y, z in cubes:
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        min_z = min(z, min_z)
        max_z = max(z, max_z)

    outside = mark_outside(min_x-1, max_x+1, min_y-1, max_y+1, min_z-1, max_z+1)
    air = set()
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                if (x, y, z) not in outside and (x, y, z) not in cubes:
                    air.add((x, y, z))

    return surface_area(cubes) - surface_area(air)


print(answer1())
print(answer2())
