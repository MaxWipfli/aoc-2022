#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

nums = [int(line) if len(line) > 0 else None for line in lines]
elf_lists = [[]]

for num in nums:
    if num is None:
        elf_lists.append([])
    else:
        elf_lists[-1].append(num)
elf_sums = [sum(l) for l in elf_lists]

print("Part 1 (maximum calories for an Elf):   ", max(elf_sums))

top_3_elf_sums = sorted(elf_sums)[-3:]

print("Part 2 (sum of calories for top 3 Elfs):", sum(top_3_elf_sums))
