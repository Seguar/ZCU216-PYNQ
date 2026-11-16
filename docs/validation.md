# Validation status

Checked 2026-11-16 against PYNQ v4.0.0 and AMD 2025.2. A complete experimental image now exists and has passed offline checks. It has not been physically boot-tested.

## Test / how

Generated the PS-only XSA with real Vivado 2025.2 and the official ZCU216 preset; ran both hardware and SDT wrapper modes inside the upstream PYNQ 4 Docker environment. Generated SDT with `zcu216-reva`, preprocessed and compiled it together with the EDF board additions, and inspected the resulting nodes. Ran the pinned PYNQ Makefile boot target in dry-run mode and hardware-free integrity checks.

## Results

All of those checks passed. The compiled DT reports ZCU216 RevA, stock 2 GiB low + 2 GiB high PS memory, 33333333 Hz PS reference clock, CLK104 bridge/clock nodes and 512 MiB CMA constrained to low memory. The new self-test IDs exist in the pinned upstream package. Historical binary bytes match the old commit; recovered clock files and their manifest remain unchanged.

SDTGen reports a fallback warning for `CONFIG.PSU__PSS_REF_CLK__FREQMHZ`; the resulting reference frequency was independently checked in the compiled DT. No firmware execution is inferred from that check. PS-only hardware export does not implement a PL design or establish RF timing.

## Conclusion / remaining work

All EDF boot/kernel/zocl/kernel-devsrc builds and complete image assembly passed. The exact assembled image passed partition bounds, FAT/ext4 integrity, boot-file comparisons, final DTB, root identity, installed dependency commit and SSH service/socket ordering checks. PYNQ 4.0.0 and RFSoC libraries imported under ARM user-mode QEMU; NumPy sum(arange(1024)) returned 523776. Seven hardware-free source/cleanup tests passed. The final Linux map exposes 4095 MiB of the stock 4 GiB.

Fresh-card boot, runtime allocation/Jupyter/overlay on the board and RF/MTS operation remain **unverified**. See the experimental release for the image, exact hashes, package inventory, kernel configuration and resolved EDF revisions. Do not call this image hardware-verified.

No running board or RFSoC configuration was changed. See `validation.json` for the machine-readable status.
