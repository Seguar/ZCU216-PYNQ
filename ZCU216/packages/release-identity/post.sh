#!/usr/bin/env bash
set -euo pipefail
target=${1:?Offline target root required}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
sudo python3 "$here/sanitize.py" "$target"
sudo install -m 0644 "$here/pynq-ssh-hostkeys.service" "$target/etc/systemd/system/pynq-ssh-hostkeys.service"
sudo systemctl --root="$target" enable pynq-ssh-hostkeys.service
