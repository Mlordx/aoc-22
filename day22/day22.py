import sys

GRID = set()
WALLS = set()
COMMANDS = ''
INITIAL_POSITION = None
INITIAL_DIRECTION = 0
DIRECTIONS = ['E', 'S', 'W', 'N']

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    read_commands = False
    for i, line in enumerate(file):
        if line == '\n':
            read_commands = True
            continue

        if read_commands:
            COMMANDS = line.strip()
            break

        stripped_line = line.strip('\n')
        for j, c in enumerate(stripped_line):
            if c == '#':
                GRID.add((j, i))
                WALLS.add((j, i))

            if c == '.':
                if INITIAL_POSITION is None:
                    INITIAL_POSITION = (j, i)

                GRID.add((j, i))


def get_next_move(commands):
    if len(commands) == 0:
        return '', ''

    i = 1
    command = commands[0]

    if command not in '0123456789':
        return command, commands[1:]

    while i < len(commands) and commands[i] != 'R' and commands[i] != 'L':
        command += commands[i]
        i += 1

    return command, commands[i:]


def get_new_position(amnt, pos):
    (x1, y1), direction = pos
    x = [x for x, y in GRID if y == y1]
    y = [y for x, y in GRID if x == x1]
    new_position = (x1, y1)
    for _ in range(amnt):
        if DIRECTIONS[direction] == 'E':
            new_x = new_position[0]+1 if new_position[0]+1 <= max(x) else min(x)
            next_position = (new_x, new_position[1])

            if next_position not in WALLS:
                new_position = next_position
            else:
                break  # hit a wall
        elif DIRECTIONS[direction] == 'S':
            new_y = new_position[1]+1 if new_position[1]+1 <= max(y) else min(y)
            next_position = (new_position[0], new_y)

            if next_position not in WALLS:
                new_position = next_position
            else:
                break  # hit a wall
        elif DIRECTIONS[direction] == 'W':
            new_x = new_position[0]-1 if new_position[0]-1 >= min(x) else max(x)
            next_position = (new_x, new_position[1])

            if next_position not in WALLS:
                new_position = next_position
            else:
                break  # hit a wall
        else:
            new_y = new_position[1]-1 if new_position[1]-1 >= min(y) else max(y)
            next_position = (new_position[0], new_y)

            if next_position not in WALLS:
                new_position = next_position
            else:
                break  # hit a wall
    return (new_position, direction)


def get_next_position_3d(pos):
    (x, y), dir = pos

    if y == 0 and 100 <= x <= 149 and DIRECTIONS[dir] == 'N':  # A Norte
        return ((x - 100, 199), DIRECTIONS.index('N'))

    if y == 199 and 0 <= x <= 49 and DIRECTIONS[dir] == 'S':  # A Sul
        return ((x + 100, 0), DIRECTIONS.index('S'))

    if x == 149 and 0 <= y <= 49 and DIRECTIONS[dir] == 'E':  # B Leste 1
        return ((99, 149 - y), DIRECTIONS.index('W'))

    if x == 99 and 100 <= y <= 149 and DIRECTIONS[dir] == 'E':  # B Leste 2
        return ((149, 149 - y), DIRECTIONS.index('W'))

    if y == 49 and 100 <= x <= 149 and DIRECTIONS[dir] == 'S':  # C Sul
        return ((99, x - 50), DIRECTIONS.index('W'))

    if x == 99 and 50 <= y <= 99 and DIRECTIONS[dir] == 'E':  # C Leste
        return ((y + 50, 49), DIRECTIONS.index('N'))

    if y == 149 and 50 <= x <= 99 and DIRECTIONS[dir] == 'S':  # D Sul
        return ((49, x + 100), DIRECTIONS.index('W'))

    if x == 49 and 150 <= y <= 199 and DIRECTIONS[dir] == 'E':  # D Leste
        return ((y - 100, 149), DIRECTIONS.index('N'))

    if y == 0 and 50 <= x <= 99 and DIRECTIONS[dir] == 'N':  # E Norte
        return ((0, 100 + x), DIRECTIONS.index('E'))

    if x == 0 and 150 <= y <= 199 and DIRECTIONS[dir] == 'W':  # E Oeste
        return ((y - 100, 0), DIRECTIONS.index('S'))

    if x == 50 and 0 <= y <= 49 and DIRECTIONS[dir] == 'W':  # F Oeste
        return ((0, 149 - y), DIRECTIONS.index('E'))

    if x == 0 and 100 <= y <= 149 and DIRECTIONS[dir] == 'W':  # F Oeste 2
        return ((50, 149 - y), DIRECTIONS.index('E'))

    if y == 100 and 0 <= x <= 49 and DIRECTIONS[dir] == 'N':  # G Norte
        return ((50, x + 50), DIRECTIONS.index('E'))

    if x == 50 and 50 <= y <= 99 and DIRECTIONS[dir] == 'W':  # G Oeste
        return ((y - 50, 100), DIRECTIONS.index('S'))

    if DIRECTIONS[dir] == 'E':
        return ((x+1, y), dir)
    if DIRECTIONS[dir] == 'S':
        return ((x, y+1), dir)
    if DIRECTIONS[dir] == 'W':
        return ((x-1, y), dir)
    if DIRECTIONS[dir] == 'N':
        return ((x, y-1), dir)


def get_new_position_3d(amnt, pos):
    new_position = pos

    for _ in range(amnt):
        next_position = get_next_position_3d(new_position)
        (x, y), _ = next_position
        assert 0 <= x <= 149 and 0 <= y <= 199

        if (x, y) not in WALLS:
            new_position = next_position
        else:
            break  # hit a wall

    return new_position


def solve(part1=True):
    moves = COMMANDS
    position = (INITIAL_POSITION, INITIAL_DIRECTION)

    while moves:
        move, moves = get_next_move(moves)

        if move[0] in '0123456789':
            move = int(move)

            if part1:
                new_position = get_new_position(move, position)
            else:
                new_position = get_new_position_3d(move, position)
        else:
            pos, dir = position
            if move == 'R':
                new_position = (pos, (dir + 1) % 4)
            else:
                new_position = (pos, (dir - 1) % 4)

        position = new_position

    (x, y), direction = position
    return 1000 * (y + 1) + 4 * (x + 1) + direction


def answer1():
    return solve()


def answer2():
    return solve(False)


print(answer1())
print(answer2())
