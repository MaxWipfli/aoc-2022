#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

# Partition input data into stack data and move data.
stack_lines = []
move_lines = []
for idx, line in enumerate(lines):
    if line == "":
        stack_lines = lines[:idx-1]
        move_lines = lines[idx+1:]

# Parse stack data.
num_stacks = len(stack_lines[-1].split(' '))
stacks = [[] for _ in range(num_stacks)]
for line in stack_lines[::-1]:
    for i in range(len(stacks)):
        if line[4*i] == '[':
            stacks[i].append(line[4*i+1])

# Parse move data.
moves = []
for line in move_lines:
    parts = line.split(' ')
    moves.append((int(parts[1]), int(parts[3]), int(parts[5])))

# Save stacks for part 2.
stacks_copy = [stack.copy() for stack in stacks]

# Part 1: Execute moves.
for num, orig, dest in moves:
    for _ in range(num):
        element = stacks[orig-1].pop()
        stacks[dest-1].append(element)

# Part 1: Calculate output.
output = [stack[-1] for stack in stacks]
output_str = ''.join(output)
print('Crates on top of each stack (part 1):', output_str)

# Part 2: Execute moves.
stacks = stacks_copy
for num, orig, dest in moves:
    # Remove from origin stack.
    elements = stacks[orig-1][-num:]
    stacks[orig-1] = stacks[orig-1][:-num]
    # Append to destination stack.
    stacks[dest-1].extend(elements)

# Part 2: Calculate output.
output = [stack[-1] for stack in stacks]
output_str = ''.join(output)
print('Crates on top of each stack (part 2):', output_str)
