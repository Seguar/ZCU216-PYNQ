#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-3-Clause
set -euo pipefail
target=${1:?Target root filesystem required}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
sudo install -d -m 0755 "$target/usr/local/share/zcu216-tics"
for file in "$here"/tics/*.txt; do
    sudo install -m 0644 "$file" "$target/usr/local/share/zcu216-tics/"
done
