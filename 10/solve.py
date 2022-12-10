#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import numpy as np

# Data Input.
with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

cycle = 1
current_addx_arg = None
current_addx_last_cycle = None
x_reg = 1

signal_strength_cycles = [20, 60, 100, 140, 180, 220]
signal_strengths = []

CRT_HEIGHT = 6
CRT_WIDTH = 40
crt = np.zeros(CRT_HEIGHT * CRT_WIDTH, dtype=bool)

iterator = iter(lines)

while True:
    # Calculate signal strengh.
    if cycle in signal_strength_cycles:
        signal_strength = cycle * x_reg
        signal_strengths.append(signal_strength)

    # Handle CRT drawing.
    # crt_index, crt_column start at 0, but cycle starts at 1.
    crt_index = cycle - 1
    if crt_index < len(crt):
        crt_column = crt_index % CRT_WIDTH
        crt[crt_index] = (abs(crt_column - x_reg) <= 1)

    # Handle instructions.
    if current_addx_arg is not None:
        # We are currently in an instruction.
        if current_addx_last_cycle == cycle:
            x_reg += current_addx_arg
        current_addx_arg = None
        current_addx_last_cycle = None
    else:
        # Fetch new instruction.
        try:
            inst = next(iterator)
        except StopIteration:
            break

        if inst == "noop":
            # Do nothing.
            pass
        else:
            parts = inst.split(' ')
            assert len(parts) == 2 and parts[0] == "addx"
            arg = int(parts[1])
            current_addx_arg = arg
            # Each 'addx' takes two cycles.
            current_addx_last_cycle = cycle + 1

    # End of cycle.
    cycle += 1

print('Program terminated, cycle =', cycle)
print('Sum of signal strengths (part 1):', sum(signal_strengths))

crt = np.reshape(crt, (CRT_HEIGHT, CRT_WIDTH))
for row in crt:
    print(*('#' if col else '.' for col in row), sep='')

