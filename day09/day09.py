import sys

commands = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        direction, amount = line.strip().split()
        commands.append((direction, int(amount)))


def move_head(position, direction):
    x, y = position
    if direction == 'U':
        return (x+1, y)
    if direction == 'D':
        return (x-1, y)
    if direction == 'L':
        return (x, y-1)
    if direction == 'R':
        return (x, y+1)


def touching(head, tail):
    x_h, y_h = head
    x_t, y_t = tail

    diff_x = abs(x_h - x_t)
    diff_y = abs(y_h - y_t)

    return diff_x <= 1 and diff_y <= 1


def move_tail(head, tail):
    x_h, y_h = head
    x_t, y_t = tail

    if touching(head, tail):
        return tail
    else:
        if x_t == x_h:
            if touching(head, (x_t, y_t+1)):
                return (x_t, y_t+1)
            else:
                return (x_t, y_t-1)

        if y_t == y_h:
            if touching(head, (x_t+1, y_t)):
                return (x_t+1, y_t)
            else:
                return (x_t-1, y_t)

        diagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for diagonal in diagonals:
            off_x, off_y = diagonal
            new_tail = (x_t + off_x, y_t + off_y)
            if touching(head, new_tail):
                return new_tail


def answer1():
    known_positions = set()
    head = (0, 0)
    tail = (0, 0)

    for command in commands:
        direction, amount = command
        for _ in range(amount):
            head = move_head(head, direction)
            tail = move_tail(head, tail)
            known_positions.add(tail)

    return len(known_positions)


def answer2():
    known_positions = set()
    knots = [(0, 0) for _ in range(10)]

    for command in commands:
        direction, amount = command

        for _ in range(amount):
            knots[0] = move_head(knots[0], direction)
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i-1], knots[i])

            known_positions.add(knots[-1])
    return len(known_positions)


print(answer1())
print(answer2())
