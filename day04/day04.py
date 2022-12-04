import sys


assignments = []

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        assignment = line.split()[0].split(',')
        (a1, b1) = assignment[0].split('-')
        (a2, b2) = assignment[1].split('-')

        assignments.append((int(a1), int(b1)))
        assignments.append((int(a2), int(b2)))


def fully_contains(interval1, interval2):
    a1, b1 = interval1
    a2, b2 = interval2

    if a1 <= a2 and b2 <= b1 or a2 <= a1 and b1 <= b2:
        return True


def overlaps(interval1, interval2):
    a1, b1 = interval1
    a2, b2 = interval2

    if a1 <= a2 and a2 <= b1 or a1 <= b2 and b2 <= b1:
        return True
    if a2 <= a1 and a1 <= b2 or a2 <= b1 and b1 <= b2:
        return True


def answer1():
    total = 0
    for i in range(0, len(assignments), 2):
        int1 = assignments[i]
        int2 = assignments[i+1]

        total += 1 if fully_contains(int1, int2) else 0

    return total


def answer2():
    total = 0
    for i in range(0, len(assignments), 2):
        int1 = assignments[i]
        int2 = assignments[i+1]

        total += 1 if overlaps(int1, int2) else 0

    return total


print(answer1())
print(answer2())
