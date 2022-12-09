#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT


def parse_line(line):
    parts = line.split(" ")
    return parts[0], int(parts[1])


def solve_part(moves, rope_length):
    rope = [(0, 0)] * rope_length

    tail_visited = set([rope[-1]])

    for direction, count in moves:
        for _ in range(count):
            # Handle one step.
            prev_rope = rope.copy()

            # Handle head.
            if direction == "L":
                rope[0] = (rope[0][0] - 1, rope[0][1])
            elif direction == "R":
                rope[0] = (rope[0][0] + 1, rope[0][1])
            elif direction == "D":
                rope[0] = (rope[0][0], rope[0][1] - 1)
            elif direction == "U":
                rope[0] = (rope[0][0], rope[0][1] + 1)
            else:
                assert False

            # For each further knot, move it according to the rules.
            for i in range(1, rope_length):
                current = rope[i]
                predecessor = rope[i - 1]

                delta_x = abs(current[0] - predecessor[0])
                delta_y = abs(current[1] - predecessor[1])
                if delta_x == 2 and delta_y == 2:
                    rope[i] = (
                        (current[0] + predecessor[0]) // 2,
                        (current[1] + predecessor[1]) // 2,
                    )
                elif delta_x == 2:
                    rope[i] = ((current[0] + predecessor[0]) // 2, predecessor[1])
                elif delta_y == 2:
                    rope[i] = (predecessor[0], (current[1] + predecessor[1]) // 2)

                # Verify the knot is still adjacent to its predecessor.
                assert (
                    abs(rope[i][0] - predecessor[0]) <= 1
                    and abs(rope[i][1] - predecessor[1]) <= 1
                )

            # Store tail position.
            tail_visited.add(rope[-1])

    return len(tail_visited)


# Data Input.
with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f]

moves = list(map(parse_line, lines))
print("Part 1:", solve_part(moves, 2))
print("Part 2:", solve_part(moves, 10))
