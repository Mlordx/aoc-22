import sys

numbers = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for unstripped_line in file:
        numbers.append(unstripped_line.strip())


translation = {
    '-': -1,
    '=': -2,
    '0': 0,
    '1': 1,
    '2': 2,
    -1: '-',
    -2: '=',
    0: '0',
    1: '1',
    2: '2'
}


def sum_snafu(number1, number2):
    n1 = number1[::-1]
    n2 = number2[::-1]

    if len(n2) > len(n1):
        n1, n2 = n2, n1

    resp = ''
    carry = '0'
    i = 0
    while True:
        if i < len(n2):
            c1, c2 = n1[i], n2[i]
            sum_chars = translation[c1] + translation[c2] + translation[carry]
        elif i < len(n1):
            c1 = n1[i]
            sum_chars = translation[c1] + translation[carry]
        else:
            if carry != '0':
                resp += carry
            break

        if sum_chars > 2:
            carry = '1'
        elif sum_chars < -2:
            carry = '-'
        else:
            carry = '0'

        resp += translation[(sum_chars + 2) % 5 - 2]
        i += 1

    return resp[::-1]


def answer1():
    total = numbers[0]
    for i in range(1, len(numbers)):
        total = sum_snafu(total, numbers[i])
    return total


print(answer1())
