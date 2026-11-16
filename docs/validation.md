# Validation status

Checked 2026-11-16 against PYNQ v4.0.0 and AMD 2025.2. This is a source-port update, not a new boot-tested image release.

## Test / how

Generated the PS-only XSA with real Vivado 2025.2 and the official ZCU216 preset; ran both hardware and SDT wrapper modes inside the upstream PYNQ 4 Docker environment. Generated SDT with `zcu216-reva`, preprocessed and compiled it together with the EDF board additions, and inspected the resulting nodes. Ran the pinned PYNQ Makefile boot target in dry-run mode and hardware-free integrity checks.

## Results

All of those checks passed. The compiled DT reports ZCU216 RevA, stock 2 GiB low + 2 GiB high PS memory, 33333333 Hz PS reference clock, CLK104 bridge/clock nodes and 512 MiB CMA constrained to low memory. The new self-test IDs exist in the pinned upstream package. Historical binary bytes match the old commit; recovered clock files and their manifest remain unchanged.

SDTGen reports a fallback warning for `CONFIG.PSU__PSS_REF_CLK__FREQMHZ`; the resulting reference frequency was independently checked in the compiled DT. No firmware execution is inferred from that check. PS-only hardware export does not implement a PL design or establish RF timing.

## Conclusion / remaining work

The modern board descriptor and wrapper are exercised through hardware/SDT generation. Full EDF boot/kernel compilation, complete image assembly, fresh-card boot, runtime allocation/Jupyter/overlay and RF/MTS operation have **not** been run for this port. Build `boot`, then `image`, inspect the final boot artifacts, and validate on the actual ZCU216 before calling a produced image hardware-verified.

No running board or RFSoC configuration was changed. See `validation.json` for the machine-readable status.
