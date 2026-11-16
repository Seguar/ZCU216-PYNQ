# SPDX-License-Identifier: BSD-3-Clause
ARCH_ZCU216 := aarch64
FPGA_MANAGER_ZCU216 := 1
# No boot overlay: legacy 2023.2 binaries are deliberately not installed as 2025.2 hardware.
STAGE4_PACKAGES_ZCU216 := pynq ethernet xrt xrfclk xrfdc xsdfec tics selftest release-identity
