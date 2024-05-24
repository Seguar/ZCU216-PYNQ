# ZCU216-PYNQ
# Preparations:

Install Vivado, Vitis and PetaLinux 2022.1
Make sure that they are in PATH

export PATH="/opt/crosstool-ng/bin:/opt/qemu/bin:$PATH"
source <vivado_settings>
source <petalinux_settings>
petalinux-util --webtalk off

sudo dpkg-reconfigure dash 
Press NO to configure bash

sudo dpkg --add-architecture i386
sudo apt update
give full rights to pynq directory
/bin/bash /pynq/sdbuild/scripts/setup_host.sh




make images BOARDS=ZCU216 PYNQ_SDIST=/prebuilt/pynq_sdist.tar.gz PYNQ_ROOTFS=/prebuilt/pynq_rootfs.aarch64.tar.gz
