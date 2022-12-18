import sys
from collections import defaultdict


adjacency = defaultdict()
pressure_release = defaultdict()
distance = defaultdict()
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for line in file:
        stripped_line = line.strip()
        source_info, destination_info = line.split(';')
        source_info, destination_info = source_info.split(), destination_info.split()

        source_valve = source_info[1]
        released_pressure = int(source_info[4].split('=')[1])
        pressure_release[source_valve] = released_pressure

        adjacency[source_valve] = []
        for destination in destination_info[4:]:
            adjacency[source_valve].append(destination.replace(',', ''))

MEMO = defaultdict()


def calculate_pressure(TOTAL_TIME, node, time, opened_nodes, pressure):
    global MEMO
    opened = frozenset(opened_nodes)

    if time == TOTAL_TIME:
        return 0

    if (node, time, opened) in MEMO:
        return MEMO[(node, time, opened)]

    max_pressure = pressure
    if node not in opened_nodes and pressure_release[node] > 0:
        new_opened = set(opened_nodes)
        new_opened.add(node)

        max_pressure = max(pressure, (TOTAL_TIME-time)*pressure_release[node] + calculate_pressure(
            TOTAL_TIME,
            node,
            time+1,
            new_opened,
            pressure
        ))

    for adj in adjacency[node]:
        adj_pressure = calculate_pressure(TOTAL_TIME, adj, time+1, set(opened_nodes), pressure)
        max_pressure = max(max_pressure, adj_pressure)

    MEMO[(node, time, opened)] = max_pressure
    return max_pressure


def answer1_v1():
    global MEMO
    MEMO = defaultdict()
    return calculate_pressure(30, 'AA', 1, set(), 0)


def compute_distances(starting_position, valid_valves):
    queue = [(starting_position, 0)]
    visited = set()

    while len(queue) > 0:
        current, dist = queue.pop(0)

        if current in visited:
            continue

        visited.add(current)
        if current != starting_position and current in valid_valves:
            distance[(starting_position, current)] = dist

        for adj in adjacency[current]:
            queue.append((adj, dist + 1))


def calculate_pressure_v2(TOTAL_TIME, valid_valves):
    memo = defaultdict(int)
    queue = [('AA', TOTAL_TIME, set(), 0)]

    while len(queue) > 0:
        current_node, remaining_time, opened, pressure = queue.pop(0)

        assert remaining_time > 0

        if pressure > memo[frozenset(opened)]:
            memo[frozenset(opened)] = pressure

        for valve in valid_valves:
            if valve in opened:
                continue
            if valve == current_node:
                if remaining_time == 0:
                    continue

                queue.append((
                    valve,
                    remaining_time-1,
                    opened | {valve},
                    pressure + (remaining_time-1)*pressure_release[valve]
                ))
            else:
                new_remaining_time = remaining_time-distance[(current_node, valve)]-1

                if new_remaining_time <= 0:
                    continue

                queue.append((
                    valve,
                    new_remaining_time,
                    opened | {valve},
                    pressure + (new_remaining_time)*pressure_release[valve]
                ))

    return memo


def answer1_v2():
    valid_valves = [key for key in pressure_release if pressure_release[key] > 0]

    for key in pressure_release:
        compute_distances(key, valid_valves)

    max_pressure_by_opened_set = calculate_pressure_v2(30, valid_valves)
    return max(max_pressure_by_opened_set.values())


def answer2():
    valid_valves = [key for key in pressure_release if pressure_release[key] > 0]

    max_pressure_by_opened_set = calculate_pressure_v2(26, valid_valves)
    answer = -1
    for s1 in max_pressure_by_opened_set.keys():
        for s2 in max_pressure_by_opened_set.keys():
            if s1.isdisjoint(s2):
                answer = max(
                    answer,
                    max_pressure_by_opened_set[s1] + max_pressure_by_opened_set[s2]
                )

    return answer


print(answer1_v1())
print(answer1_v2())
print(answer2())
