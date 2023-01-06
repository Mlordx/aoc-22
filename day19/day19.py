import sys
from collections import defaultdict
from copy import deepcopy


class Blueprint():
    def __init__(self, ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost):
        self.ore_cost = ore_robot_cost
        self.clay_cost = clay_robot_cost
        self.obsidian_cost = obsidian_robot_cost
        self.geode_cost = geode_robot_cost

    def _can_build(self, resource_name, resource_count):
        if resource_name == 'ore':
            if resource_count['ore'] >= self.ore_cost:
                return True

        if resource_name == 'clay':
            if resource_count['ore'] >= self.clay_cost:
                return True

        if resource_name == 'obsidian':
            ore_cost, clay_cost = self.obsidian_cost
            if resource_count['ore'] >= ore_cost and resource_count['clay'] >= clay_cost:
                return True

        if resource_name == 'geode':
            ore_cost, obsidian_cost = self.geode_cost
            if resource_count['ore'] >= ore_cost and resource_count['obsidian'] >= obsidian_cost:
                return True

        return False

    def get_robot_options(self, resource_count):
        options = set()

        if self._can_build('geode', resource_count):
            # always go for geode if possible
            return set(['geode'])

        if self._can_build('ore', resource_count):
            options.add('ore')

        if self._can_build('clay', resource_count):
            options.add('clay')

        if self._can_build('obsidian', resource_count):
            options.add('obsidian')

        return options

    def build_robot(self, resource_name, resource_count, robots):
        new_resource_count = deepcopy(resource_count)
        new_robots = deepcopy(robots)

        if resource_name == 'ore':
            new_resource_count['ore'] -= self.ore_cost
            new_robots['ore'] += 1

        if resource_name == 'clay':
            new_resource_count['ore'] -= self.clay_cost
            new_robots['clay'] += 1

        if resource_name == 'obsidian':
            ore_cost, clay_cost = self.obsidian_cost
            new_resource_count['ore'] -= ore_cost
            new_resource_count['clay'] -= clay_cost
            new_robots['obsidian'] += 1

        if resource_name == 'geode':
            ore_cost, obsidian_cost = self.geode_cost
            new_resource_count['ore'] -= ore_cost
            new_resource_count['obsidian'] -= obsidian_cost
            new_robots['geode'] += 1

        return new_resource_count, new_robots

    def get_max_robots(self):
        max_ore = max([self.ore_cost, self.clay_cost, self.obsidian_cost[0], self.geode_cost[0]])
        max_clay = self.obsidian_cost[1]
        max_obsidian = self.geode_cost[1]
        max_geode = int(1e12)

        return {'ore': max_ore, 'clay': max_clay, 'obsidian': max_obsidian, 'geode': max_geode}


blueprints = []
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'r') as file:
    for unsplit_line in file:
        line = unsplit_line.split()
        blueprints.append(
            Blueprint(
                int(line[6]),
                int(line[12]),
                (int(line[18]), int(line[21])),
                (int(line[27]), int(line[30]))
            )
        )


def get_snapshot(elapsed_time, resources, robots, skipped_building):
    r1, r2, r3, r4 = resources.values()
    rb1, rb2, rb3, rb4 = robots.values()

    return (elapsed_time, r1, r2, r3, r4, rb1, rb2, rb3, rb4, frozenset(skipped_building))


def calculate_max_geodes(total_time, blueprint):
    resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
    robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    starting_state = (0, resources, robots, set())
    stack = [starting_state]
    best = defaultdict(int)
    max_robots = blueprint.get_max_robots()
    seen = set()

    while stack:
        elapsed_time, resources, robots, skipped_building = stack.pop()

        snapshot = get_snapshot(elapsed_time, resources, robots, skipped_building)
        if snapshot in seen:
            continue

        seen.add(snapshot)

        best[elapsed_time] = max(best[elapsed_time], resources['geode'])

        t = total_time - elapsed_time
        if best[elapsed_time] >= resources['geode'] + robots['geode']*t + t*(t-1)/2:
            # current state's potential is lower than theoretical max
            continue

        if elapsed_time < total_time:
            options = blueprint.get_robot_options(resources)

            if 'geode' not in options:
                stack.append((elapsed_time+1, get_resources(resources, robots), robots, options))

            for option in options:
                if robots[option]+1 > max_robots[option]:
                    continue
                elif option in skipped_building:
                    continue
                else:
                    new_resources, new_robots = blueprint.build_robot(
                        option,
                        resources,
                        robots
                    )

                    stack.append(
                        (elapsed_time+1, get_resources(new_resources, robots), new_robots, set())
                    )

    return best[total_time]


def get_resources(resources, robots):
    new_resources = deepcopy(resources)

    for rock_type, amount in robots.items():
        new_resources[rock_type] += amount
        if new_resources[rock_type] >= 70:
            new_resources[rock_type] = 70

    return new_resources


def answer1():
    total = 0
    for i, blueprint in enumerate(blueprints):
        max_geodes = calculate_max_geodes(24, blueprint)
        total += (i+1) * max_geodes

    return total


def answer2():
    total = 1
    for _, blueprint in enumerate(blueprints[:3]):
        max_geodes = calculate_max_geodes(32, blueprint)
        total *= max_geodes

    return total


print(answer1())
print(answer2())
