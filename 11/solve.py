#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import copy
import math
import numpy as np

class Monkey:
    def __init__(self, items, operation, divisor, true_next, false_next):
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.true_next = true_next
        self.false_next = false_next
        self.inspection_count = 0

    # Iterates over (item, next).
    # If there is no worryness_modulus, this means that worryness is divided by three each round.
    def do_turn(self, worryness_modulus=None):
        while len(self.items) > 0:
            item = self.items.pop(0)
            # Apply operation.
            item = self._apply_operation(item)

            if worryness_modulus is not None:
                # Keep worryness level manageable by reducing mod 'worryness_modulus'.
                item = item % worryness_modulus
            else:
                # Divide worryness level by 3.
                item = item // 3

            self.inspection_count += 1

            if item % self.divisor == 0:
                yield item, self.true_next
            else:
                yield item, self.false_next

    def receive_item(self, item):
        self.items.append(item)

    def _apply_operation(self, item):
        if self.operation == "* old":
            return item * item
        elif self.operation[0] == "*":
            return item * int(self.operation.split(" ")[1])
        elif self.operation[0] == "+":
            return item + int(self.operation.split(" ")[1])
        else:
            assert False, "Not implemented."


def run_part(monkeys, num_rounds, do_divide=False):
    worryness_modulus = None
    if not do_divide:
        worryness_modulus = math.lcm(*(monkey.divisor for monkey in monkeys))
    for round in range(num_rounds):
        for i in range(len(monkeys)):
            print(f'Round {round}, monkey {i}')
            for item, next_monkey in monkeys[i].do_turn(worryness_modulus=worryness_modulus):
                monkeys[next_monkey].receive_item(item)

    inspection_counts = [monkey.inspection_count for monkey in monkeys]
    inspection_counts.sort()
    return inspection_counts[-2] * inspection_counts[-1]


monkeys_part1 = []

# Data input and parsing.
with open("input.txt") as f:
    while True:
        # 'Monkey 0'
        assert next(f).startswith("Monkey ")
        # 'Starting items: 79, 98'
        items = [int(x) for x in next(f).split(':')[1].strip().split(', ')]
        # 'Operation: new = old * 19'
        operation = next(f).split('old ', maxsplit=1)[1].strip()
        # 'Test: divisible by 23'
        divisor = int(next(f).strip().split(' ')[-1])
        # 'If true: throw to monkey 2'
        true_next = int(next(f).strip().split(' ')[-1])
        # 'If false: throw to monkey 3'
        false_next = int(next(f).strip().split(' ')[-1])
        monkeys_part1.append(Monkey(items, operation, divisor, true_next, false_next))
        # Empty line.
        try:
            assert next(f) == '\n', "Empty line expected."
        except StopIteration:
            break

monkeys_part2 = copy.deepcopy(monkeys_part1)

# Part 1.
result = run_part(monkeys_part1, 20, do_divide=True)
print('Level of monkey business (part 1):', result)
# Part 2.
result = run_part(monkeys_part2, 10000, do_divide=False)
print('Level of monkey business (part 2):', result)
