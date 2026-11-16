#!/usr/bin/env bash
set -euo pipefail
target=${1:?Offline target root required}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo=$(cd "$here/../../.." && pwd)
sudo install -m 0644 "$repo/docs/build-inputs.json" "$target/usr/local/share/zcu216-build-inputs.json"
