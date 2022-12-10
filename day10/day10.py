import sys
from collections import defaultdict

addition_by_cycle = defaultdict()

commands = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        split_line = line.strip().split()
        if len(split_line) > 1:
            commands.append(int(split_line[1]))
        else:
            commands.append(0)

    addition_by_cycle[1] = 1
    current_cycle = 2

    for command in commands:
        if command == 0:
            current_cycle += 1
            continue
        else:
            addition_by_cycle[current_cycle] = command
            current_cycle += 2


def cycle_value(chosen_cycle):
    total = 0
    for cycle, amount in addition_by_cycle.items():
        if cycle < chosen_cycle:
            total += amount
    return total


def answer1():
    interesting_values = [20, 60, 100, 140, 180, 220]
    strength = 0

    for interesting_value in interesting_values:
        strength += interesting_value * cycle_value(interesting_value)

    return strength


def print_screen(screen):
    resp = ''
    for line in screen:
        for c in line:
            resp += c
        resp += '\n'

    print(resp)


def answer2():
    screen = [['.' for _ in range(40)] for _ in range(6)]
    current_cycle = 1
    for i in range(len(screen)):
        for j in range(len(screen[0])):
            if abs(cycle_value(current_cycle) - j) <= 1:
                screen[i][j] = '#'
            current_cycle += 1

    print_screen(screen)


print(answer1())
answer2()
