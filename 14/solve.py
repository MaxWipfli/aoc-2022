#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import numpy as np


def generate_field(structures, x_min, x_max, y_max, floor=False):
    x_size = x_max - x_min + 1
    y_size = y_max + 3
    field = np.zeros((x_size, y_size), dtype=np.int8)

    for points in structures:
        last_point = points[0]
        for i in range(1, len(points)):
            point = points[i]
            # x-coordinate is constant.
            if point[0] == last_point[0]:
                y1 = min(last_point[1], point[1])
                y2 = max(last_point[1], point[1])
                field[point[0] - x_min, y1 : y2 + 1] = 1
            else:
                x1 = min(last_point[0], point[0]) - x_min
                x2 = max(last_point[0], point[0]) - x_min
                field[x1 : x2 + 1, point[1]] = 1
            last_point = point

    if floor:
        field[:, y_max + 2] = 1
    return field


def print_field(field):
    for y in range(field.shape[1]):
        for x in range(field.shape[0]):
            if field[x][y] == 0:
                print(".", end="")
            elif field[x][y] == 1:
                print("#", end="")
            else:
                print("o", end="")
        print()


# Read input.
with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

structures = []
x_coords = []
y_coords = []

for line in lines:
    points = line.split(" -> ")
    points = [tuple(int(x) for x in point.split(",")) for point in points]
    structures.append(points)
    for x, y in points:
        x_coords.append(x)
        y_coords.append(y)

# Add one empty column on either side.
x_min = min(x_coords) - 1
x_max = max(x_coords) + 1
y_min = 0
y_max = max(y_coords)

field = generate_field(structures, x_min, x_max, y_max, floor=False)

# Simulate.
sand_start = (500 - x_min, 0)
resting_sand_count = 0
flows_into_abyss = False

while not flows_into_abyss:
    x_sand, y_sand = sand_start
    while True:
        if y_sand == field.shape[1] - 1:
            flows_into_abyss = True
            break
        if field[x_sand, y_sand + 1] == 0:
            y_sand += 1
        elif field[x_sand - 1, y_sand + 1] == 0:
            x_sand -= 1
            y_sand += 1
        elif field[x_sand + 1, y_sand + 1] == 0:
            x_sand += 1
            y_sand += 1
        else:
            # Sand comes to rest.
            field[x_sand][y_sand] = 2
            resting_sand_count += 1
            break

print("Part 1:", resting_sand_count)


# Part 2.
# The sand will create a triangle. The triangle will be completely filled with sand, except if
# (1) the block is occupied by a structure,
# (2) sand does not flow into the block.
# The second case only occurs if the three cells directly and diagonally above the cell aren't
# filled with sand.

y_floor = y_max + 2
triangle_height = y_floor

x_min = min(x_min, 500 - triangle_height)
x_max = max(x_max, 500 + triangle_height)

field = generate_field(structures, x_min, x_max, y_max, floor=True)

# Scan through the full triangle, and count cells aren't filled with sand.
# At the beginning, x=500, y=0 is filled with sand.
field[500 - x_min, 0] = 2
resting_sand_count = 1

for y in range(1, y_floor):
    for x in range(500 - x_min - y, 500 - x_min + y + 1):
        if field[x][y] == 1:
            # Filled with structure.
            continue
        if field[x - 1][y - 1] == 2 or field[x][y - 1] == 2 or field[x + 1][y - 1] == 2:
            field[x][y] = 2
            resting_sand_count += 1

print("Part 2:", resting_sand_count)
