#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

from enum import Enum
from functools import cmp_to_key
import sys


def tokenize(list_str):
    tokens = []
    current_num = None
    for char in list_str:
        if char in ['[', ',', ']']:
            if current_num:
                tokens.append(int(current_num))
                current_num = None
            tokens.append(char)
        elif current_num is None:
            current_num = char
        else:
            current_num += char
    if current_num:
        tokens.append(int(current_num))
        current_num = None
    return tokens


def print_tokens(tokens):
    for token in tokens:
        token_str = str(token)
        if len(token_str) == 1:
            print(token_str, ' ', sep='', end='')
        else:
            print(token_str, end='')
        print(' ', end='')
    print()


def has_correct_order(left, right):
    left_list_closings = 0
    right_list_closings = 0

    left = tokenize(left)
    right = tokenize(right)

    left_it = iter(left)
    right_it = iter(right)

    i = 0
    while True:
        if left_list_closings > 0:
            left_next = ']'
            left_list_closings -= 1
        else:
            try:
                left_next = next(left_it)
            except StopIteration:
                return True
        if right_list_closings > 0:
            right_next = ']'
            right_list_closings -= 1
        else:
            try:
                right_next = next(right_it)
            except StopIteration:
                return False

        # Handle int, not-int cases first, as they fall through.
        if type(left_next) == int and type(right_next) != int:
            # int, (one of '[', ']')
            while right_next == '[':
                # int, list
                assert right_list_closings == 0
                left_list_closings += 1
                right_next = next(right_it)
            if right_next == ']':
                return False
        elif type(left_next) != int and type(right_next) == int:
            # (one of '[', ']'), int
            while left_next == '[':
                # list, int
                assert left_list_closings == 0
                right_list_closings += 1
                left_next = next(left_it)
            if left_next == ']':
                return True

        if type(left_next) == int and type(right_next) == int:
            # int, int
            if left_next < right_next:
                return True
            if left_next > right_next:
                return False
            continue
        if left_next == right_next:
            # both are either '[', ',', ']', but both are the same
            continue
        # both of them are either '[', ',' or ']', but not both the same.
        if right_next == ']':
            return False
        if left_next == ']':
            return True
        assert False


with open('input.txt' if len(sys.argv) == 1 else 'sample_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

# Part 1
pairs = []
for i in range(0, len(lines), 3):
    pairs.append(lines[i:i+2])

right_order_indices = []
for i, pair in enumerate(pairs):
    if has_correct_order(*pair):
        right_order_indices.append(i + 1)
print('Sum of indices of correct pairs (part 1):', sum(right_order_indices))

# Part 2
FIRST_DIVIDER = '[[2]]'
SECOND_DIVIDER = '[[6]]'

lines = list(filter(lambda line: line != '', lines)) + [FIRST_DIVIDER, SECOND_DIVIDER]
key_fn = cmp_to_key(lambda x, y: -1 if has_correct_order(x, y) else 1)
lines.sort(key=key_fn)
first_div = lines.index(FIRST_DIVIDER) + 1
second_div = lines.index(SECOND_DIVIDER) + 1
print('Decoder key (part 2):', first_div * second_div)
