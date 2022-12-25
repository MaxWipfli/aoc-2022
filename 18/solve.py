#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import sys


def neighbors(cube):
    x, y, z = cube
    return [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)]


OUTSIDE = (-1, -1, -1)
can_reach_outside_cache = dict()
def can_reach_outside(cubes, target):
    global can_reach_outside_cache
    assert target not in cubes
    try:
        return can_reach_outside_cache[target]
    except KeyError:
        pass

    visited = set()
    to_visit = [target]
    visited_and_to_visit = set(to_visit)

    while to_visit:
        current = to_visit.pop(0)
        visited.add(current)
        if current == OUTSIDE:
            # We reached OUTSIDE.
            for point in visited:
                can_reach_outside_cache[point] = True
            return True

        for neighbor in neighbors(current):
            if neighbor in cubes:
                continue
            if neighbor in visited_and_to_visit:
                continue
            to_visit.append(neighbor)
            visited_and_to_visit.add(neighbor)

    # We reached a dead end, without visiting OUTSIDE. We are inside.
    for point in visited:
        can_reach_outside_cache[point] = False
    return False


use_sample = len(sys.argv) > 1

with open("sample_input.txt" if use_sample else "input.txt") as f:
    cubes = set(tuple(int(x) for x in line.rstrip('\n').split(',')) for line in f)

# Part 1.
surface_faces = 0
for cube in cubes:
    for neighbor in neighbors(cube):
        surface_faces += int(neighbor not in cubes)
print('Part 1:', surface_faces)

# Part 2.
surface_faces = 0
for cube in cubes:
    for neighbor in neighbors(cube):
        surface_faces += int((neighbor not in cubes) and can_reach_outside(cubes, neighbor))
print('Part 2:', surface_faces)