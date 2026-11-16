# ZCU216-PYNQ

ZCU216 board port targeting **PYNQ 4.0.0**, Ubuntu 24.04 / Python 3.12, and **AMD 2025.2 EDF**. PetaLinux is not used by the current build.

**Status: source port / hardware-description validated; no new SD image or ZCU216 boot/RF validation is claimed.** The old deployed PYNQ 3.0.1 beamforming installation and its recovered clock files remain documented under [runtime/beamforming](runtime/beamforming/README.md).

## Current port

- PYNQ submodule pinned to v4.0.0, commit `d90670c69f7b71ea1a5d23aaa3e0ec713ff5fa9f`.
- Custom EDF machine generated from a fresh Vivado 2025.2 PS-only XSA and the official ZCU216 RevA board preset/SDT.
- Stock **4 GiB PS DDR**, with the high DDR bank limited to the actual remaining 2 GiB.
- CLK104 I2C-to-SPI bridge, kernel driver and clock-table delivery through version-independent package paths.
- Standard PYNQ 4 RFSoC libraries and non-RF image self-tests.

This is a **bring-your-own-application-overlay** image port. The historical 2023.2.2 base overlay is not silently installed as 2025.2 hardware. Its bit/HWH/XSA bytes are preserved under [legacy/overlays/base](legacy/overlays/base), with hashes in [docs/legacy-artifacts.json](docs/legacy-artifacts.json). MTS wrapper/API migration and RF performance require separate validation; old binary overlays and patches are not assumed compatible with PYNQ 4.

## Build

Use an x86-64 Linux build machine, Docker, compatible Vivado/Vitis **2025.2** installations with ZU49DR support, and at least 100 GB free disk (more is useful). AMD tools/licenses must be obtained separately.

```sh
git clone --recurse-submodules https://github.com/Seguar/ZCU216-PYNQ.git
cd ZCU216-PYNQ
./scripts/prepare.sh
export XILINX_TOOLS=/tools/Xilinx/2025.2
export XILINXD_LICENSE_FILE="$HOME/.Xilinx"
./scripts/build.sh hardware
./scripts/build.sh sdt
```

For a complete image, put the official PYNQ 4.0.0 AArch64 rootfs and source distribution in `PYNQ/sdbuild/prebuilt`, named `pynq_rootfs.aarch64.tar.gz` and `pynq_sdist.tar.gz`. Obtain them from [pynq.io](https://www.pynq.io/) or rebuild using upstream instructions. Record their checksums for the build.

```sh
./scripts/build.sh boot   # EDF boot components, kernel, DT and zocl
./scripts/build.sh image  # complete SD image
```

Default output: `PYNQ/sdbuild/output/ZCU216-4.0.0.img`. See [build details](docs/build.md), [pinned inputs](docs/build-inputs.json) and [validation](docs/validation.md). No image is attached to a new release until a build exists and its validation level is recorded.

## Existing beamforming deployment

[Runtime snapshot](runtime/beamforming/README.md) records the inspected PYNQ 3.0.1 installation, recovered LMK/LMX tables, application repository, and Vivado 2023.2.2 boundary. Those recovered tables remain byte-preserved and separate from image defaults. Nothing in this source update programs RF clocks, installs a live board, flashes an SD card, or proves MTS/calibration compatibility.

The historical PetaLinux recipe, old host setup script and patches are under [legacy](legacy/README.md). Do not mix them into the EDF build.

## References

- [PYNQ v4.0.0 release](https://github.com/Xilinx/PYNQ/releases/tag/v4.0.0)
- [PYNQ 4 external-board build system](https://github.com/Xilinx/PYNQ/blob/v4.0.0/sdbuild/BUILD_SYSTEM.md)
- [RFSoC-PYNQ](https://github.com/Xilinx/RFSoC-PYNQ/tree/v4.0.0)
- [AMD ZCU216 PS DDR specification](https://docs.amd.com/r/en-US/ug1390-zcu216-eval-bd/PS-DDR4-SODIMM-Socket)
