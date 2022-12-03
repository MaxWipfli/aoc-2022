#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

def read_lines():
    with open('input.txt') as f:
        return [line.rstrip('\n') for line in f]


def get_priority(char):
    if char.islower():
        return ord(char) - ord('a') + 1
    else:
        return ord(char) - ord('A') + 27


lines = read_lines()

# Part 1
priority_sum = 0
for rucksack in lines:
    length = len(rucksack)
    part1 = rucksack[:length//2]
    part2 = rucksack[length//2:]
    assert len(part1) == len(part2)
    types1 = set(part1)
    types2 = set(part2)
    common = list(types1.intersection(types2))
    assert len(common) == 1
    priority_sum += get_priority(common[0])
print('Priority sum (part 1):', priority_sum)

# Part 2
it = iter(lines)
triples = zip(it, it, it)

priority_sum = 0
for r1, r2, r3 in triples:
    common = list(set(r1).intersection(set(r2)).intersection(set(r3)))
    assert len(common) == 1
    priority_sum += get_priority(common[0])
print('Priority sum (part 2):', priority_sum)
