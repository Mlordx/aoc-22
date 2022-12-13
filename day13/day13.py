import sys
import ast
import functools

packets = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        if line == '\n':
            continue
        else:
            packets.append(ast.literal_eval(line.strip()))


def compare_packets(value1, value2):
    if type(value1) == int and type(value2) == int:
        if value1 < value2:
            return 1
        if value1 > value2:
            return -1
        return 0

    if type(value1) == list and type(value2) == list:
        if len(value1) == 0 and len(value2) > 0:
            return 1

        if len(value2) == 0 and len(value1) > 0:
            return -1

        if len(value1) == 0 and len(value2) == 0:
            return 0

        comparison = compare_packets(value1[0], value2[0])
        if comparison == 0:
            return compare_packets(value1[1:], value2[1:])
        else:
            return comparison

    if type(value1) == int:
        return compare_packets([value1], value2)

    return compare_packets(value1, [value2])


def answer1():
    total = 0

    for i in range(0, len(packets), 2):
        p1 = packets[i]
        p2 = packets[i+1]

        if compare_packets(p1, p2) == 1:
            total += i//2 + 1

    return total


def answer2():
    packets.append([[2]])
    packets.append([[6]])

    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare_packets), reverse=True)
    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)


print(answer1())
print(answer2())
