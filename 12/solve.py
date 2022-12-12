#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import numpy as np
from functools import reduce


def dijkstra(matrix, start, is_end, iter_neighbors):
    unvisited_set = set(np.ndindex(data.shape))
    inf_value = reduce(lambda x, y: x * y, matrix.shape) * 10
    distances = np.full_like(matrix, inf_value)
    distances[start] = 0
    current = start

    while True:
        for neighbor in iter_neighbors(current):
            distances[neighbor] = min(distances[neighbor], distances[current] + 1)
        unvisited_set.remove(current)
        if is_end(current):
            return distances[current]
        # Find unvisited node with smallest tenative distance.
        candidate_node = None
        candidate_distance = inf_value
        for node in unvisited_set:
            if distances[node] < candidate_distance:
                candidate_node = node
                candidate_distance = distances[node]
        if candidate_distance == inf_value:
            return None
        current = candidate_node


# Read input.
with open("input.txt") as f:
    data = np.array([[ord(c) for c in line.strip()] for line in f], np.short)

# Find start and end points.
start = None
end = None
for idx in np.ndindex(data.shape):
    if start and end:
        break
    if data[idx] == ord("S"):
        data[idx] = ord("a")
        start = idx
    if data[idx] == ord("E"):
        data[idx] = ord("z")
        end = idx
assert start is not None and end is not None

# Helper function to iterate over all neighbors of a node, i.e. all valid adjacent indices which
# fulfill the height difference condition.
def iter_neighbors(node):
    neighbors = [
        (node[0] - 1, node[1]),
        (node[0] + 1, node[1]),
        (node[0], node[1] - 1),
        (node[0], node[1] + 1),
    ]

    for neighbor in neighbors:
        if not (0 <= neighbor[0] < data.shape[0] and 0 <= neighbor[1] < data.shape[1]):
            continue
        # Valid adjacent node. Check if we can move there.
        # We move from end to start rather than start to end.
        # This means we cannot descend more than 1 height unit, but ascend arbitrarily many units.
        if data[neighbor] - data[node] >= -1:
            yield neighbor


# We go from end to start rather than start to end. Thus, switch start and end points.
path_length = dijkstra(data, end, lambda x: x == start, iter_neighbors)
print("Path length (part 1):", path_length)
path_length = dijkstra(data, end, lambda x: data[x] == ord("a"), iter_neighbors)
print("Path length (part 2):", path_length)
