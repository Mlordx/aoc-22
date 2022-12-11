class Monkey:
    def __init__(self, items_held, operation, test, if_true, if_false):
        self.items_held = items_held
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.business_level = 0

    def inspection(self, divide_worry=True):
        while len(self.items_held) > 0:
            self.business_level += 1
            old = self.items_held.pop(0)
            new = eval(self.operation)
            divided_by = 3 if divide_worry else 1

            if (new//divided_by) % self.test == 0:
                self.throw(self.if_true, (new//divided_by))
            else:
                self.throw(self.if_false, (new//divided_by))

    def throw(self, target, item):
        monkeys[target].receive(item)

    def receive(self, item):
        self.items_held.append(item)

modulo = 11 * 17 * 5 * 13 * 19 * 2 * 3 * 7
monkeys = []


def reset_monkeys():
    global monkeys
    monkeys = [
        Monkey([98, 97, 98, 55, 56, 72], '(old%modulo) * 13', 11, 4, 7),
        Monkey([73, 99, 55, 54, 88, 50, 55], '(old%modulo) + 4', 17, 2, 6),
        Monkey([67, 98], '(old%modulo) * 11', 5, 6, 5),
        Monkey([82, 91, 92, 53, 99], '(old%modulo) + 8', 13, 1, 2),
        Monkey([52, 62, 94, 96, 52, 87, 53, 60], '(old%modulo) * (old%modulo)', 19, 3, 1),
        Monkey([94, 80, 84, 79], '(old%modulo) + 5', 2, 7, 0),
        Monkey([89], '(old%modulo) + 1', 3, 0, 5),
        Monkey([70, 59, 63], '(old%modulo) + 3', 7, 4, 3),
    ]


def answer1():
    reset_monkeys()
    for _ in range(20):
        for i in range(len(monkeys)):
            monkeys[i].inspection()

    business_levels = sorted([monkey.business_level for monkey in monkeys], reverse=True)
    return business_levels[0] * business_levels[1]


def answer2():
    reset_monkeys()
    for _ in range(10000):
        for i in range(len(monkeys)):
            monkeys[i].inspection(False)

    business_levels = sorted([monkey.business_level for monkey in monkeys], reverse=True)
    return business_levels[0] * business_levels[1]


print(answer1())
print(answer2())
