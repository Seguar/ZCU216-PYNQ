# ZCU216 beamforming runtime snapshot — 2026-11-15

The inspected ZCU216 RevA runs **PYNQ 3.0.1**, with xrfclk 2.0 and xrfdc 2.0.
Its selected notebook and overlay are maintained in
[doa_rfsoc, zcu216 branch](https://github.com/Seguar/doa_rfsoc/tree/zcu216/PS/python/beamforming).
That snapshot is the strongest recent-use candidate from saved execution and
modification metadata; the board clock is incorrect, so calendar dates and
definitive last-use attribution remain uncertain.

The runtime wrapper selects **LMK 500 MHz / LMX 2000 MHz**. The two files in
[clocks](clocks) were copied byte-for-byte from the installed xrfclk package;
[manifest.json](clocks/manifest.json) records their SHA-256 hashes. These are
register configurations, not measured clock frequencies.

The recovered `LMK04828_500.0.txt` differs from `ZCU216/tics/LMK04828_500.0.txt`.
The original image-build clock files are retained. This runtime snapshot is
deliberately outside `ZCU216/tics`, so building an image does not silently change
its clock configuration. For this deployment, back up the installed register
files and explicitly install the two recovered files into the board's xrfclk
package directory after checking the connected clock hardware. The inspected
directory was `/usr/local/share/pynq-venv/lib/python3.10/site-packages/xrfclk`.
The collection itself did not install or apply clock files.

## Toolchain boundaries

- The current repository targets PYNQ 4.0.0 / AMD 2025.2 EDF; historical PYNQ 3.0.1 / 2022.1 instructions are archived under `legacy/`. This runtime snapshot remains the original 3.0.1 deployment and is not a PYNQ 4 validation.
- The recovered application HWH declares **Vivado 2023.2.2**. Application overlay
  version and SD-image build version are separate facts.
- The available build VM has **2025.2**. A new image or overlay build requires
  an explicit port or matching legacy tools; this audit did not perform one.
- Matching Python version strings do not prove that local xrfclk/xrfdc patches
  are reproduced. The patched libraries were not reconstructed in this audit.

## Validation

Confirmed board/package identity and recovered register-file hashes. Notebook
dependencies and the bit/hwh pair are archived in doa_rfsoc. No image rebuild,
boot test, clock measurement, or hardware programming was performed. Calibration
files remain installation-specific; follow the application snapshot README.
