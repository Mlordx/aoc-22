import sys
import copy


stacks = [[] for _ in range(9)]
commands = []

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    reading_crates = True

    for line in file:
        if line == '\n':
            reading_crates = False
            continue
        if reading_crates:
            for i in range(1, len(line), 4):
                if line[i] not in "123456789[]\n ":
                    stacks[(i-1)//4].insert(0, line[i])
        else:
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
