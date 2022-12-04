#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

def read_lines():
    with open('input.txt') as f:
        return [line.rstrip('\n') for line in f]


def contains(range1, range2):
    return range1[0] <= range2[0] and range2[1] <= range1[1]


def do_overlap(range1, range2):
    # Check for non-overlapping ranges, then invert.
    return not (range1[1] < range2[0] or range2[1] < range1[0])


lines = read_lines()

data = [[tuple(int(x) for x in part.split('-')) for part in line.split(',')] for line in lines]

# Part 1
fully_contained = sum(contains(r1, r2) or contains(r2, r1) for r1, r2 in data)
print('Fully contained ranges (part 1):', fully_contained)

# Part 2
overlapping = sum(do_overlap(*ranges) for ranges in data)
print('Overlapping ranges (part 2):', overlapping)
