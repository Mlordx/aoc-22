import sys
from collections import defaultdict


class Directory:
    def __init__(self, name, parent, dir_size):
        self.name = name
        self.parent = parent
        self.children = []
        self.dir_size = dir_size

    def add_child(self, dir):
        self.children.append(dir)

    def total_size(self):
        total = self.dir_size
        for child in self.children:
            total += child.total_size()

        return total

    def add_file(self, size):
        self.dir_size += size


directory_info = defaultdict()
directory_info['/'] = Directory('/', None, 0)


def dir_name(dir_tree):
    name = dir_tree[0]
    for dir in dir_tree[1:]:
        name += '-' + dir

    return name


input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    dir_tree = []

    for unstripped_line in file:
        line = unstripped_line.strip()
        command = line[0:4]
        if command == '$ cd':
            cd_argument = line[4:].strip()

            if cd_argument == '..':
                dir_tree.pop()
            else:
                dir_tree.append(cd_argument)
            continue

        elif command == '$ ls':
            continue

        elif command == 'dir ':
            name = line[4:].strip()
            new_dir = Directory(dir_name(dir_tree+[name]), dir_name(dir_tree), 0)
            directory_info[dir_name(dir_tree+[name])] = new_dir
            directory_info[dir_name(dir_tree)].add_child(new_dir)
        else:
            size = int(line.split()[0])
            directory_info[dir_name(dir_tree)].add_file(size)


def answer1():
    total = 0
    for dir in directory_info:
        dir_size = directory_info[dir].total_size()
        total += dir_size if dir_size <= 100000 else 0

    return total


def answer2():
    max_size = 70000000
    needed_unused_space = 30000000
    used_space = directory_info['/'].total_size()
    current_unused_space = max_size - used_space

    min_size = 2 ** 32
    for dir in directory_info:
        dir_size = directory_info[dir].total_size()
        if current_unused_space + dir_size >= needed_unused_space:
            min_size = min(min_size, dir_size)

    return min_size


print(answer1())
print(answer2())
