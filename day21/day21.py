import sys
from copy import deepcopy

operations = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for unstripped_line in file:
        line = unstripped_line.strip().replace(':', '=')
        operations.append(line)


def compute(operations):
    operations_here = deepcopy(operations)
    for op in operations_here:
        try:
            exec(op)
        except NameError:
            operations_here.append(op)
            continue

    return eval('root')


def answer1():
    return int(compute(operations))


def answer2():
    real_operations = []
    for op in operations:
        if 'root' in op:
            real_operations.append(op.replace('+', '-'))
        elif op[:4] != 'humn':
            real_operations.append(op)

    lo = int(0)
    hi = int(1e13)
    while True:
        num = (lo + hi) // 2
        result = compute(real_operations + [f'humn = {num}'])

        if result > 0:
            lo = num + 1
        elif result < 0:
            hi = num - 1
        else:
            return num


print(answer1())
print(answer2())
