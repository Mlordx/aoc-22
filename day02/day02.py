import sys

translation = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
}

points = {
    'A': 1,
    'B': 2,
    'C': 3,
}

loses_to = {
    'A': 'C',
    'B': 'A',
    'C': 'B',
}

beats = {
    'A': 'B',
    'B': 'C',
    'C': 'A'
}

rounds = []

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        a, b = line.split()
        rounds.append((a, b))


def score(you, opp):
    result = 0
    if you == opp:
        result = 3
    elif you == beats[opp]:
        result = 6
    else:
        result = 0

    return points[you] + result


def answer1():
    total = 0
    for r in rounds:
        a, b = r
        total += score(translation[b], a)

    return total


def answer2():
    total = 0
    for r in rounds:
        a, b = r
        if b == 'X':
            total += score(loses_to[a], a)
        elif b == 'Y':
            total += score(a, a)
        else:
            total += score(beats[a], a)

    return total


print(answer1())
print(answer2())
