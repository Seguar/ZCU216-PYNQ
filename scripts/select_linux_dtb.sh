#!/usr/bin/env bash
# Upstream v4 extraction skips symlinks and can pick a regular U-Boot DTB.
set -euo pipefail
repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
deploy="$repo/PYNQ/sdbuild/edf-cache/pynq-edf/build/tmp/deploy/images/zynqmp-zcu216-pynq"
source_dtb="$deploy/system.dtb"
destination="$repo/PYNQ/sdbuild/output/boot/ZCU216/system.dtb"
test -f "$source_dtb" || { echo "Linux system.dtb missing: $source_dtb" >&2; exit 2; }
mkdir -p "$repo/work"
python3 "$repo/scripts/check_boot_dtb.py" "$source_dtb" > "$repo/work/boot-dtb-validation.json"
if ! cmp -s "$source_dtb" "$destination"; then cp -L "$source_dtb" "$destination"; fi
cmp "$source_dtb" "$destination"
echo 'ZCU216 Linux DTB selected and validated'
