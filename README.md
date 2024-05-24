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

/bin/bash /pynq/sdbuild/scripts/setup_host.sh



