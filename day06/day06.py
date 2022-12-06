import sys

LINE = ''

input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        LINE = line.strip()


def answer1():
    for i in range(3, len(LINE)):
        if len(set(LINE[i-3:i+1])) == 4:
            return i+1


def answer2():
    for i in range(13, len(LINE)):
        if len(set(LINE[i-13:i+1])) == 14:
            return i+1


print(answer1())
print(answer2())
