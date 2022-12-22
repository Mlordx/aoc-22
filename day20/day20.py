import sys
from copy import deepcopy

numbers = []
ZERO_ORIGINAL_INDEX = -1
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for i, unstripped_line in enumerate(file):
        numbers.append((int(unstripped_line.strip()), i))
        if int(unstripped_line) == 0:
            ZERO_ORIGINAL_INDEX = i


def update_list(number_list, i):
    number, original_index = number_list[i]
    new_list = number_list[:i] + number_list[i+1:]
    new_index = (i + number) % len(new_list)
    new_list.insert(new_index, (number, original_index))
    return new_list


def answer1():
    current_numbers = deepcopy(numbers)

    for num in numbers:
        index = current_numbers.index(num)
        current_numbers = update_list(current_numbers, index)

    index_of_zero = current_numbers.index((0, ZERO_ORIGINAL_INDEX))
    total = 0
    for offset in [1000, 2000, 3000]:
        total += current_numbers[(index_of_zero+offset) % len(current_numbers)][0]

    return total


def answer2():
    current_numbers = [(num*811589153, index) for num, index in numbers]

    for _ in range(10):
        for num in numbers:
            number, i = num
            index = current_numbers.index((number*811589153, i))
            current_numbers = update_list(current_numbers, index)

    index_of_zero = current_numbers.index((0, ZERO_ORIGINAL_INDEX))
    total = 0
    for offset in [1000, 2000, 3000]:
        total += current_numbers[(index_of_zero+offset) % len(current_numbers)][0]
    return total


print(answer1())
print(answer2())
