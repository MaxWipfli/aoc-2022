#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import itertools
import numpy as np
import sys


use_sample = len(sys.argv) > 1

with open("sample_input.txt" if use_sample else "input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

valves = []
for line in lines:
    parts = line.split(" ")
    name = parts[1]
    flow_rate = int(line.split("=")[1].split(";")[0])
    connections = [name.strip(",") for name in parts[9:]]
    valves.append((name, flow_rate, connections))

name_to_idx = {name: idx for idx, (name, _, _) in enumerate(valves)}

# Find all-pairs shortest paths (Floyd-Warshall).
inf_value = 10**9
num_nodes = len(valves)
distances = np.ones((num_nodes, num_nodes), dtype=np.int32) * inf_value
for name, _, connections in valves:
    for neighbor_name in connections:
        i1 = name_to_idx[name]
        i2 = name_to_idx[neighbor_name]
        distances[i1][i2] = 1
for i in range(num_nodes):
    distances[i][i] = 0
for k in range(num_nodes):
    for i in range(num_nodes):
        for j in range(num_nodes):
            if distances[i][j] > distances[i][k] + distances[k][j]:
                distances[i][j] = distances[i][k] + distances[k][j]

# Now, construct a new, fully-connected graph. Add 1 to each edge weight to
# account for the minute to open the valve. We never need to transit any valve,
# as we can move directely between nodes. We don't need to store the
# adjacencies, as their are implicit (fully-connected).
distances += 1

# Remove all nodes with 0 flow from the graph (except AA, the starting point).
nodes = np.array(
    [
        idx
        for idx, (name, flow_rate, _) in enumerate(valves)
        if name == "AA" or flow_rate > 0
    ]
)

# Use indexing into flows, so also keep flows from pruned nodes.
flows = np.array([flow for _, flow, _ in valves])
max_flow = np.sum(flows)


def get_total_flow_part1(time_left, curr_node, nodes_visited, acc_flow):
    cand_flow = -1
    time_step_flow = np.dot(nodes_visited, flows)
    for adj_node in nodes:
        if nodes_visited[adj_node]:
            continue
        if time_left < distances[curr_node][adj_node]:
            continue
        new_visited = np.copy(nodes_visited)
        new_visited[adj_node] = True
        new_flow = get_total_flow_part1(
            time_left - distances[curr_node][adj_node],
            adj_node,
            new_visited,
            acc_flow + time_step_flow * distances[curr_node][adj_node],
        )
        if new_flow > cand_flow:
            cand_flow = new_flow
    if cand_flow == -1:
        # Base case. No candidate. Just stay here.
        return acc_flow + time_step_flow * time_left
    else:
        return cand_flow


# Part 1
nodes_visited = np.zeros(num_nodes, dtype=bool)
flow = get_total_flow_part1(30, name_to_idx["AA"], nodes_visited, 0)
print("Part 1:", flow)

# Part 2
print("Part 2: I got too annoyed to do this. Let's move on...")
