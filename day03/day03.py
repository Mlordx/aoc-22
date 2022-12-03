import sys


rucksacks = []

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        rucksacks.append(line)


def priority(char):
    if char in 'abcdefghijklmnopqrstuvwxyz':
        return ord(char) - 96
    else:
        return ord(char) - 38


def answer1():
    total = 0
    for rucksack in rucksacks:
        length = len(rucksack.strip())
        A = set(rucksack[:length//2])
        B = set(rucksack[length//2:])
        (intersection,) = A.intersection(B)
        total += priority(intersection)

    return total


def answer2():
    total = 0

    for i in range(0, len(rucksacks), 3):
        A = set(rucksacks[i].strip())
        B = set(rucksacks[i+1].strip())
        C = set(rucksacks[i+2].strip())

        for char in A:
            if char in A.intersection(B) and char in A.intersection(C):
                total += priority(char)

    return total


print(answer1())
print(answer2())
