#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

from pprint import pprint


def get_dir(tree, fragments):
    current = tree
    for frag in fragments:
        current = current[frag]
    return current
with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]


def get_size(item, dirsize_cb):
    if type(item) == int:
        return item
    elif type(item) == dict:
        size = sum(get_size(child, dirsize_cb) for child in item.values())
        dirsize_cb(size)
        return size


# list of (command, [lines of output])
commands = []

for line in lines:
    if line.startswith('$'):
        commands.append((line, []))
    else:
        commands[-1][1].append(line)

# list of fragments, i.e. ['usr', 'bin'] for '/usr/bin'.
cwd = []
tree = {}

for command, output in commands:
    if command.startswith("$ cd"):
        # Handle 'cd' command.
        arg = command.split(" ")[2]
        if arg == "..":
            cwd.pop()
        elif arg == "/":
            cwd.clear()
        else:
            cwd.append(arg)
    elif command == "$ ls":
        # Handle ls command.
        for line in output:
            info, name = line.split(' ')
            cwd_dir = get_dir(tree, cwd)
            if name in cwd_dir:
                # Do nothing.
                pass
            elif info == "dir":
                cwd_dir[name] = {}
            else:
                cwd_dir[name] = int(info)
    else:
        assert False

dir_sizes = []
root_dir_size = get_size(tree, lambda size: dir_sizes.append(size))


# Part 1
small_dirs = [size for size in dir_sizes if size <= 100000]
print('Sum of directories with size <= 100000 (part 1):', sum(small_dirs))


# Part 2
total_space = 70000000
space_needed = 30000000
free_space = total_space - root_dir_size
space_needed -= free_space

# target: smallest dir size >= space_needed
target = None
for size in dir_sizes:
    if size < space_needed:
        continue
    if target is None or size < target:
        target = size

print('Size of most viable directory to delete (part 2):', target)
