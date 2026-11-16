#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
expected=d90670c69f7b71ea1a5d23aaa3e0ec713ff5fa9f
test -e "$repo/PYNQ/.git" || { echo 'Run git submodule update --init --recursive first' >&2; exit 2; }
test "$(git -C "$repo/PYNQ" rev-parse HEAD)" = "$expected" || { echo 'Unexpected PYNQ submodule revision' >&2; exit 2; }
tools=${XILINX_TOOLS:-/tools/Xilinx/2025.2}
license_dir=${XILINXD_LICENSE_FILE:-"$HOME/.Xilinx"}
image=${PYNQ_DOCKER_IMAGE:-pynqdock:zcu216-4.0.0}
test -f "$tools/Vivado/settings64.sh" && test -f "$tools/Vitis/settings64.sh" || { echo 'Set XILINX_TOOLS to the installed 2025.2 tool root' >&2; exit 2; }
test -e "$license_dir" || { echo 'This wrapper expects an existing license file/directory' >&2; exit 2; }
mode=${1:-image}
case "$mode" in image|boot|hardware|sdt) ;; *) echo 'Usage: build.sh [image|boot|hardware|sdt]' >&2; exit 2;; esac
security=()
if [[ -n "${APPARMOR_PROFILE:-}" ]]; then security=(--security-opt "apparmor=$APPARMOR_PROFILE"); fi
docker run --init --rm --network host --privileged "${security[@]}" \
    -e XILINX_TOOLS="$tools" -e XILINXD_LICENSE_FILE="$license_dir" -e BUILD_MODE="$mode" \
    -e BOARD=ZCU216 -e PYNQ_BOARDNAME=ZCU216 -e FPGA_MANAGER=1 \
    -v "$tools:$tools:ro" -v "$license_dir:$license_dir:ro" -v "$repo:/port" \
    "$image" bash -c '
        set -eo pipefail
        if [[ "$BUILD_MODE" = image ]]; then sudo python3 /port/scripts/register_qemu.py; fi
        export PYNQ_BOARDNAME=ZCU216 FPGA_MANAGER=1
        before=$(sha256sum /port/ZCU216/hardware/ps.xsa 2>/dev/null || true)
        make -C /port/ZCU216/hardware
        after=$(sha256sum /port/ZCU216/hardware/ps.xsa)
        if [[ "$before" != "$after" ]]; then touch /port/ZCU216/edf.env; fi
        if [[ "$BUILD_MODE" = hardware ]]; then exit 0; fi
        if [[ "$BUILD_MODE" = sdt ]]; then
            sdtgen -xsa /port/ZCU216/hardware/ps.xsa -dir /port/work/sdt -board_dts zcu216-reva
            exit
        fi
        cd /port/PYNQ/sdbuild
        make BOARDS=ZCU216 BOARDDIR=/port boot_ZCU216
        /port/scripts/select_linux_dtb.sh
        if [[ "$BUILD_MODE" = image ]]; then
            make BOARDS=ZCU216 BOARDDIR=/port
        fi
    '
