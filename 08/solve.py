#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import numpy as np


def iter_from(x, y, direction, shape):
    if direction == "N":
        x -= 1
        while x >= 0:
            yield x, y
            x -= 1
    elif direction == "S":
        x += 1
        while x < shape[0]:
            yield x, y
            x += 1
    elif direction == "W":
        y -= 1
        while y >= 0:
            yield x, y
            y -= 1
    elif direction == "E":
        y += 1
        while y < shape[1]:
            yield x, y
            y += 1
    else:
        assert False


# Data Input.
with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

data = np.array([[int(x) for x in line] for line in lines])
visible = np.zeros_like(data, dtype=bool)

# Part 1.
# Look through all rows.
for row in range(data.shape[0]):
    # From left.
    max_height = -1
    for col in range(data.shape[1]):
        if data[row][col] > max_height:
            visible[row][col] = True
            max_height = data[row][col]
    # From right.
    max_height = -1
    for col in range(data.shape[1] - 1, -1, -1):
        if data[row][col] > max_height:
            visible[row][col] = True
            max_height = data[row][col]

# Look through all columns.
for col in range(data.shape[1]):
    # From top.
    max_height = -1
    for row in range(data.shape[0]):
        if data[row][col] > max_height:
            visible[row][col] = True
            max_height = data[row][col]
    # From right.
    max_height = -1
    for row in range(data.shape[0] - 1, -1, -1):
        if data[row][col] > max_height:
            visible[row][col] = True
            max_height = data[row][col]

count = np.sum(visible)
print("Count of visible trees (part 1):", count)

# Part 2.
def get_scenic_score(x, y):
    height = data[x][y]
    score = 1
    for direction in ["N", "S", "W", "E"]:
        distance = 0
        for row, col in iter_from(x, y, direction, data.shape):
            distance += 1
            if data[row][col] >= height:
                break
        score *= distance
        if score == 0:
            break
    return score


max_score = 0
for x, y in np.ndindex(*data.shape):
    score = get_scenic_score(x, y)
    if score > max_score:
        max_score = score

print("Maximum scenic score (part 2):", max_score)
