#!/usr/bin/env bash
set -euo pipefail
target=${1:?Offline root required}
"$ROOTDIR/packages/pynq/post.sh" "$target"
sudo unlink "$target/root/pynq-package-stage.sh"
