#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

# self, other are in [1 (rock), 2 (paper), 3 (scissors)]
def score_round(self, other):
    shape_score = self
    # +1 if won, 0 if draw, -1 if lost
    outcome_indicator = ((self - other + 1) % 3) - 1
    outcome_score = (outcome_indicator + 1) * 3
    return shape_score + outcome_score

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

chars = [line.split(' ') for line in lines]
rounds = [(ord(first) - ord('A') + 1, ord(second) - ord('X') + 1)
    for first, second in chars]

# First part
total_score = 0
for other, self in rounds:
    total_score += score_round(self, other)
print(f'Total score (part 1): {total_score}')

# Second part
# outcome: X = 1 -> loose, Y = 2 -> draw, Z = 3 -> win
total_score = 0
for other, outcome in rounds:
    # tmp is congruent to what we need to choose, mod 3.
    tmp = (other + outcome - 2) % 3
    self = (tmp - 1) % 3 + 1
    total_score += score_round(self, other)
print(f'Total score (part 2): {total_score}')
