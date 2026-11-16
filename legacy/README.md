# Historical PYNQ 3.0.1 material

These files are retained for recovery and comparison, not used by the current PYNQ 4 / EDF port.

- `build-3.0.1.md`: prior manual PetaLinux 2022.1 instructions and old compiled-image link.
- `plnx-env-setup.sh`: old host-mutating setup script. Do not run it for the current build.
- `petalinux_bsp/`: old kernel/device-tree patches; they are not EDF configuration.
- `packages/`: old xrfclk and xrfdc/MTS patches, not assumed compatible with current C/Python APIs.
- `overlays/base/`: historical bit/HWH/XSA files, byte-preserved. HWH declares Vivado 2023.2.2. They are outside the active board directory so PYNQ does not install them as current overlays.

The git history still contains the original layout. See `docs/legacy-artifacts.json` and `runtime/beamforming` for hashes and deployment provenance. Do not substitute these artifacts for a new, matched hardware build without validation.
