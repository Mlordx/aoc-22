file = open("input.txt", "r")

calories_per_elf = []

calories = 0
for line in file:
    if line == '\n':
        calories_per_elf.append(calories)
        calories = 0
        continue
    else:
        calories += int(line)


def answer1():
    return max(calories_per_elf)


def answer2():
    return sum(sorted(calories_per_elf, reverse=True)[0:3])


print(answer1())
print(answer2())
