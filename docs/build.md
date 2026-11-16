# EDF build details

The current entry point is `scripts/build.sh`, using the pinned PYNQ submodule. It exports board identity and FPGA-manager mode and generates boot hardware before invoking EDF. It deliberately does not use the legacy `.bsp`, PetaLinux patches or checked-in old overlay.

## Hardware and machine

`ZCU216/hardware/export.tcl` requires Vivado 2025.2, `xczu49dr-ffvf1760-2-e`, and `xilinx.com:zcu216:part0:2.0`. It applies the official PS preset and exports a PS-only XSA. This does not implement or time an RF/PL overlay; there is no fabricated bitstream/timing claim.

`ZCU216/edf.env` uses `EDF_MODE=custom` and machine `zynqmp-zcu216-pynq`. The pinned AMD EDF manifest has a prebuilt ZCU208 machine but no prebuilt ZCU216 machine. Do not substitute the ZCU208 machine: part, board peripherals and memory must match ZCU216.

SDTGen uses `zcu216-reva`; the stock PS memory is 4 GiB. `EDF_DDR_HIGH_BANK_REG` preserves 2 GiB low + 2 GiB high rather than an architectural-max memory size. Boards with a different installed SODIMM require a reviewed memory configuration.

The board DTS adds a 512 MiB low-memory CMA pool and CLK104's SC18IS602B bridge with LMK and separate ADC/DAC LMX chip-selects. `kernel.cfg` enables the bridge and I2C mux support. Final kernel/device-tree builds remain a separate validation gate from SDT generation.

## Tools and container

`prepare.sh` checks the pinned submodule and builds the upstream Ubuntu 24.04 Docker environment. `build.sh` expects `XILINX_TOOLS` to contain `Vivado/settings64.sh` and `Vitis/settings64.sh`, and `XILINXD_LICENSE_FILE` to be an existing license file/directory mounted at the same path. `PYNQ_DOCKER_IMAGE` overrides the image name.

On a host whose AppArmor policy blocks BitBake user namespaces, set `APPARMOR_PROFILE` to an appropriately scoped build-container profile. Do not disable host protection globally. EDF source/download/shared-state caches are kept under the PYNQ build tree; use a dedicated tree and do not run two writers on its custom-machine layer.

Use `hardware`, `sdt`, `boot`, then `image` to separate failures. Changes to the XSA touch the board EDF configuration so Make reruns the boot target. If reusing an old tree, follow upstream device-tree/shared-state invalidation rather than accepting stale board identity or FPGA-manager settings.

## Packages and clocks

The board package order installs `xrfclk` before `tics`. Clock tables are located using the active Python environment, not a hardcoded Python 3.10 path. Copying the tables does not program the clock hardware. The recovered application-specific tables under `runtime/beamforming` are not substituted for image defaults.

The archived xrfclk reload and xrfdc MTS patches target older APIs/structures. They are not applied to current driver sources. Do not reuse an old CFFI MTS structure against a new RFDC driver without validating its exact C ABI and call signatures. Hardware clock setup, SYSREF and MTS need the intended RF overlay, compatible bindings and explicit hardware tests.

## Checks and delivery

Run `python3 scripts/check_port.py` for submodule, memory-policy, legacy isolation, recovered-clock integrity and self-test-ID checks. `pynq-selftest` on a future installed image runs the board's non-RF manifest; it does not establish RF functionality or program clocks by default.

Before advertising an image as boot-tested: inspect final DT identity/RAM/UART/PHY/CLK104/CMA and zocl policy, flash a measured-capacity card with full readback checksum, capture a fresh ZCU216 boot, and exercise PYNQ/Jupyter with an explicitly compatible overlay. Do not use another board's default hostname or address as unique identity.

## Public-image identity

The final `release-identity` package removes inherited SSH host keys, known user authentication/history files, DHCP leases, machine ID and random seed from the offline build root. It sets hostname `pynq-zcu216` and enables key generation as a requirement of both SSH service and socket, so each installed board gets its own host keys before SSH accepts connections. Factory PYNQ credentials remain `xilinx` / `xilinx`; change them on first use. This does not touch a running board.

The wrapper explicitly selects the Linux `deploy/.../system.dtb` symlink after EDF completes. Upstream v4's extraction loop skips symlinks and can otherwise select a regular U-Boot DTB. `check_boot_dtb.py` checks board identity, memory, console, CLK104, CMA and absence of an enabled PL interrupt controller before that DTB is copied into the boot output and the image is assembled. In the first build the Linux and U-Boot DTBs were byte-identical; the explicit selection avoids relying on that coincidence. The generated Linux CPU memory map may expose 4095 MiB of the stock 4 GiB (its low bank is `0x7ff00000`); the upper bank remains limited to 2 GiB. No memory beyond the installed SODIMM is advertised.

The board's `pynq` package delegates to upstream but pins its PYNQ-Metadata and PYNQ-Utils Git installs to the exact revisions in `build-inputs.json`. Rendering refuses unexpected upstream URLs instead of silently building a different dependency set. The upstream submodule remains unchanged. Other installed package versions are recorded with the release artifacts.

Equal package versions can hide a different prebuilt wheel. The Git installs therefore force replacement without replacing the whole dependency set, and the final release package verifies both installed `direct_url.json` commit IDs against the manifest, repairing a mismatch before image assembly. The manifest is retained at `/usr/local/share/zcu216-build-inputs.json`.

For image mode, the privileged wrapper registers the container's static AArch64 QEMU interpreter with binfmt flag `F`. This keeps the interpreter available across chroot/mount namespaces, without relying on an executable inside the target root. A conflicting or disabled existing PYNQ entry is rejected rather than silently overwritten. The registration is in the Linux build VM, not an FPGA board.
