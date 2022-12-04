#!/bin/sh
# SPDX-FileCopyrightText: 2022 Max Wipfli <mail@maxwipfli.ch>
# SPDX-License-Identifier: MIT

script_dir="$(dirname "$0")"
cookie_file="$script_dir/cookie.txt"

if [ ! -e "$cookie_file" ]; then
    echo "Error: File 'cookie.txt' does not exist in script directory." \
        > /dev/stderr
    exit 1
fi

curl "https://adventofcode.com/2022/day/$1/input" \
    -b "session=$(cat "$cookie_file")"
