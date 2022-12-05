import sys
import copy


stacks = [
    ['W', 'R', 'F'],
    ['T', 'H', 'M', 'C', 'D', 'V', 'W', 'P'],
    ['P', 'M', 'Z', 'N', 'L'],
    ['J', 'C', 'H', 'R'],
    ['C', 'P', 'G', 'H', 'Q', 'T', 'B'],
    ['G', 'C', 'W', 'L', 'F', 'Z'],
    ['W', 'V', 'L', 'Q', 'Z', 'J', 'G', 'C'],
    ['P', 'N', 'R', 'F', 'W', 'T', 'V', 'C'],
    ['J', 'W', 'H', 'G', 'R', 'S', 'V']
]
commands = []

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    start_reading = False

    for line in file:
        if line == '\n':
            start_reading = True
            continue
        if start_reading:
            broken_line = line.split()
            qty, i, j = int(broken_line[1]), int(broken_line[3]) - 1, int(broken_line[5]) - 1
            commands.append((qty, i, j))


def moves(s, qty, i, j, part=1):
    elements = []

    for q in range(qty):
        elements.append(s[i].pop())

    if part == 1:
        for el in elements:
            s[j].append(el)
    else:
        for el in elements[::-1]:
            s[j].append(el)


def answer1():
    my_stacks = copy.deepcopy(stacks)
    for qty, i, j in commands:
        moves(my_stacks, qty, i, j)

    resp = ''
    for stack in my_stacks:
        resp += stack[-1]

    return resp


def answer2():
    my_stacks = copy.deepcopy(stacks)
    for qty, i, j in commands:
        moves(my_stacks, qty, i, j, 2)

    resp = ''
    for stack in my_stacks:
        resp += stack[-1]

    return resp


print(answer1())
print(answer2())
