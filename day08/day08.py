import sys

GRID = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for i, line in enumerate(file):
        GRID.append([])
        for j, num in enumerate(line.strip()):
            GRID[i].append(num)


def visible_from_outside(i, j):
    global GRID
    if i == 0 or j == 0:
        return True

    else:
        from_left = True
        for a in range(0, i):
            if GRID[a][j] >= GRID[i][j]:
                from_left = False

        from_right = True
        for a in range(i+1, len(GRID[0])):
            if GRID[a][j] >= GRID[i][j]:
                from_right = False

        from_top = True
        for b in range(0, j):
            if GRID[i][b] >= GRID[i][j]:
                from_top = False

        from_bottom = True
        for b in range(j+1, len(GRID)):
            if GRID[i][b] >= GRID[i][j]:
                from_bottom = False

        return from_right or from_left or from_top or from_bottom


def scenic_score(i, j):
    global GRID

    if i == 0 or j == 0:
        return 0
    else:
        visible_top = 0
        for a in range(i-1, -1, -1):
            visible_top += 1
            if GRID[a][j] >= GRID[i][j]:
                break

        visible_bottom = 0
        for a in range(i+1, len(GRID[0])):
            visible_bottom += 1
            if GRID[a][j] >= GRID[i][j]:
                break

        visible_left = 0
        for b in range(j-1, -1, -1):
            visible_left += 1
            if GRID[i][b] >= GRID[i][j]:
                break

        visible_right = 0
        for b in range(j+1, len(GRID)):
            visible_right += 1
            if GRID[i][b] >= GRID[i][j]:
                break

        return visible_right * visible_left * visible_top * visible_bottom


def answer1():
    global GRID
    total = 0

    for i in range(len(GRID[0])):
        for j in range(len(GRID)):
            total += 1 if visible_from_outside(i, j) else 0

    return total


def answer2():
    best = -1

    for i in range(len(GRID[0])):
        for j in range(len(GRID)):
            best = max(best, scenic_score(i, j))

    return best


print(answer1())
print(answer2())
