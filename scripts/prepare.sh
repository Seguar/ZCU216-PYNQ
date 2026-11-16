#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
git -C "$repo" submodule update --init --recursive
expected=d90670c69f7b71ea1a5d23aaa3e0ec713ff5fa9f
test "$(git -C "$repo/PYNQ" rev-parse HEAD)" = "$expected"
python3 "$repo/scripts/check_port.py"
docker build --build-arg USERNAME="$(id -un)" --build-arg USER_UID="$(id -u)" --build-arg USER_GID="$(id -g)" \
    -t "${PYNQ_DOCKER_IMAGE:-pynqdock:zcu216-4.0.0}" "$repo/PYNQ/sdbuild"
mkdir -p "$repo/PYNQ/sdbuild/prebuilt"
echo 'Install the official PYNQ 4.0.0 AArch64 rootfs and SDIST into PYNQ/sdbuild/prebuilt before an image build.'
