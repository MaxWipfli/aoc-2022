#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import numpy as np
import sys


use_sample = len(sys.argv) > 1

with open("sample_input.txt" if use_sample else "input.txt") as f:
    movements = list(f.readline().rstrip("\n"))

# We define, for the whole code:
# - first coordinate direction (x) is horizontal (left is negative, right is positive)
# - second coordinate direction (y) is vertical (up is positive, down is negative)

rocks = [
    ([[1, 0, 0, 0]] * 4),
    ([0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0] * 4),
    ([1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0]),
    ([1] * 4, [0] * 4, [0] * 4, [0] * 4),
    ([1, 1, 0, 0], [1, 1, 0, 0], [0] * 4, [0] * 4),
]

rock_widths = [4, 3, 3, 1, 2]
rock_heights = [1, 3, 3, 4, 2]

rocks = [np.array(rock, dtype=bool) for rock in rocks]


def print_rock(rock):
    for y in range(rock.shape[1] - 1, -1, -1):
        for x in range(rock.shape[0]):
            if rock[x][y]:
                print("#", end="")
            else:
                print(".", end="")
        print()


def collides(playing_field, rock, rock_pos):
    if rock_pos[0] < 0 or rock_pos[0] >= playing_field.shape[0] or rock_pos[1] < 0:
        return True
    for x, y in np.ndindex(*rock.shape):
        if not rock[x][y]:
            continue
        field_x = rock_pos[0] + x
        field_y = rock_pos[1] + y
        if not (
            0 <= field_x < playing_field.shape[0]
            and 0 <= field_y < playing_field.shape[1]
        ):
            # Rock part outside playing field.
            return True
        if playing_field[field_x, field_y]:
            return True
    return False


NUM_ROCKS = 10**12
FIELD_WIDTH = 7
FIELD_HEIGHT = 1000000
height_to_add = None

playing_field = np.zeros((FIELD_WIDTH, FIELD_HEIGHT), dtype=bool)
rock_level_offset = 0
highest_rock_level = -1
rock_idx = -1  # incremented before new rock spawns
movement_idx = 0  # incremented when consumed
curr_rock_pos = None
rocks_left = NUM_ROCKS

states = dict()
NUM_TOP_ROWS = 100

while (rocks_left) > 0:
    if curr_rock_pos is None:
        # Spawn new rock.
        rock_idx = (rock_idx + 1) % len(rocks)
        # Two units from left edge, and 4 units above highest rock
        # (i.e. three units empty).
        curr_rock_pos = (2, highest_rock_level + 4)

    # Apply gas jet movement.
    movement = movements[movement_idx]
    movement_idx = (movement_idx + 1) % len(movements)
    if movement == "<":
        new_rock_pos = (curr_rock_pos[0] - 1, curr_rock_pos[1])
    elif movement == ">":
        new_rock_pos = (curr_rock_pos[0] + 1, curr_rock_pos[1])
    if not collides(playing_field, rocks[rock_idx], new_rock_pos):
        curr_rock_pos = new_rock_pos

    # Move down, if possible.
    new_rock_pos = (curr_rock_pos[0], curr_rock_pos[1] - 1)
    # First comparison is prerequiste for collides() to be True.
    if new_rock_pos[1] <= highest_rock_level and collides(
        playing_field, rocks[rock_idx], new_rock_pos
    ):
        # Rock comes to rest in current position. Add it to field.
        rock = rocks[rock_idx]
        for x, y in np.ndindex(*rock.shape):
            if not rock[x, y]:
                continue
            field_x = curr_rock_pos[0] + x
            field_y = curr_rock_pos[1] + y
            playing_field[field_x, field_y] = True
        highest_rock_level = max(
            highest_rock_level, curr_rock_pos[1] + rock_heights[rock_idx] - 1
        )
        curr_rock_pos = None
        rocks_left -= 1

        rocks_done = NUM_ROCKS - rocks_left
        if rocks_done == 2022:
            print("Part 1:", highest_rock_level + rock_level_offset + 1)

        # If not already found the period, save the "state" in the state dictionary.
        if rocks_done >= 2022 and not height_to_add:
            top_rows = playing_field[
                highest_rock_level - NUM_TOP_ROWS + 1 : highest_rock_level + 1
            ]
            state = list(top_rows.flatten())
            state.append(rock_idx)
            state.append(movement_idx)
            state = tuple(state)
            try:
                prev_highest_rock_level, prev_rocks_done = states[state]
                # The state has already occured previously. Skip ahead.
                rock_level_delta = highest_rock_level - prev_highest_rock_level
                num_rocks_in_period = rocks_done - prev_rocks_done

                full_periods_left = rocks_left // num_rocks_in_period
                height_to_add = full_periods_left * rock_level_delta
                rocks_left -= full_periods_left * num_rocks_in_period
            except KeyError:
                # The state has never occured previously. Save it.
                states[state] = (highest_rock_level, rocks_done)
    else:
        curr_rock_pos = new_rock_pos

    if curr_rock_pos and curr_rock_pos[1] >= 0.75 * FIELD_HEIGHT:
        # Move everything down by half the playing field height.
        delta = FIELD_HEIGHT // 2
        print(f"Moved down by {delta} units")
        rock_level_offset += delta
        highest_rock_level -= delta
        playing_field[:, :delta] = playing_field[:, delta : 2 * delta]
        playing_field[:, delta:] = False
        curr_rock_pos = (curr_rock_pos[0], curr_rock_pos[1] - delta)

print("Part 2:", highest_rock_level + rock_level_offset + 1 + height_to_add)
