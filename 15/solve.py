#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

import numpy as np
import time


with open("input.txt", "r") as f:
    lines = [line.rstrip("\n") for line in f]

count = len(lines)
sensors = np.zeros((count, 2), dtype=np.int32)
beacons = np.zeros((count, 2), dtype=np.int32)

for i, line in enumerate(lines):
    parts = line.split("=")
    sensor = (int(parts[1].split(",")[0]), int(parts[2].split(":")[0]))
    beacon = (int(parts[3].split(",")[0]), int(parts[4]))
    sensors[i] = sensor
    beacons[i] = beacon

# For each sensor, calculate the distance to the closest beacon.
distances = np.sum(np.absolute(sensors - beacons), axis=1)

# Find size of full field.
x_min = np.min(sensors[:, 0] - distances)
x_max = np.max(sensors[:, 0] + distances)
y_min = np.min(sensors[:, 1] - distances)
y_max = np.max(sensors[:, 1] + distances)
x_size = x_max - x_min + 1
y_size = y_max - y_min + 1


def get_exclusion_region(y_target):
    # centers (offset such that x_range becomes [0, x_size))
    region_centers = sensors[:, 0] - x_min
    # extents:
    # ..... extent -1 (none)
    # ..#.. extent 0
    # .###. extent 1
    # and so on...
    y_diffs = np.absolute(sensors[:, 1] - y_target)
    region_extents = distances - y_diffs

    # Determine union of regions.
    region_counts = np.zeros(y_size, dtype=np.int8)

    for i in range(len(region_centers)):
        center = region_centers[i]
        extent = region_extents[i]
        if extent < 0:
            continue
        region_counts[center - extent : center + extent + 1] += 1
    return region_counts


# Scan one row (constant y).
y_target = 2000000
region = get_exclusion_region(y_target) > 0
# Remove all fields which have beacons.
for x, y in beacons:
    if y == y_target:
        region[x - x_min] = 0
# Count fields.
field_count = np.sum(region)
print(f"Field counts in row y={y_target} (part 1):", field_count)


# Part 2.
x_max = 4000000
y_max = 4000000

candidate = np.array([0, 0], dtype=np.int32)
x_threshold = 1000
found = False
while True:
    if candidate[0] >= x_threshold:
        print(candidate)
        x_threshold += 1000

    modified = False
    for i in range(len(sensors)):
        sensor = sensors[i]
        sensor_distance = distances[i]
        delta = np.abs(candidate - sensor)
        # If we're not blocked by this sensor, continue.
        if np.sum(delta) > sensor_distance:
            continue
        # This sensor blocks the current candidate.
        # Calculate how far to advance.
        extent = np.abs(sensor_distance - delta[0])
        # Update x coordinate to outside of extent.
        candidate[1] = sensor[1] + extent + 1
        modified = True
        if candidate[1] >= y_max:
            candidate[1] = 0
            candidate[0] += 1
    if not modified:
        break

print("Position (part 2):", candidate)
print("Tuning frequency (part 2):", (candidate[0] * 4000000) + position[1])
