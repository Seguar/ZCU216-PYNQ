#!/usr/bin/env bash
set -euo pipefail
target=${1:?Offline root required}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo=$(cd "$here/../../.." && pwd)
"$ROOTDIR/packages/pynq/pre.sh" "$target"
python3 "$repo/scripts/pin_pynq_stage.py" "$ROOTDIR/packages/pynq/qemu.sh" | sudo tee "$target/root/pynq-package-stage.sh" >/dev/null
