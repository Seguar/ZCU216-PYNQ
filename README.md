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


sudo chmod -R 777 PYNQ/
wget https://xilinx-ax-dl.entitlenow.com/dl/ul/2022/10/25/R210705180/jammy.aarch64.3.0.1.tar.gz?hash=fbmhVxZu_vOh35J4wzJRGA&expires=1716575881&filename=jammy.aarch64.3.0.1.tar.gz pynq_rootfs.aarch64.tar.gz
wget https://files.pythonhosted.org/packages/4c/d4/3a6d15a95d0d6bb47e08f7c3189595f8d20a560560c81de08fb68b624a68/pynq-3.0.1.tar.gz pynq_sdist.tar.gz

make images BOARDS=ZCU216 PYNQ_SDIST=/prebuilt/pynq_sdist.tar.gz PYNQ_ROOTFS=/prebuilt/pynq_rootfs.aarch64.tar.gz
