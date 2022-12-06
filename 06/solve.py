#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

def get_end_of_marker_index(data, marker_length):
    for i in range(len(data)):
        section = data[i:i+marker_length]
        if len(set(section)) == marker_length:
            return i + marker_length
    assert False


with open('input.txt') as f:
    data = f.read().rstrip('\n')

print('start-of-packet (part 1):', get_end_of_marker_index(data, 4))
print('start-of-message (part 2):', get_end_of_marker_index(data, 14))
