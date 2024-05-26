# ZCU216-PYNQ
[PYNQ 3.0.1 for ZCU216 compiled image](https://drive.google.com/file/d/1p9I-GHuvxmw-IJPbIhEwCG40TPVRwWEb/view?usp=sharing)

[xrfclk-patch for PYNQ](https://github.com/Xilinx/RFSoC-PYNQ/tree/master/boards/RFSoC4x2/packages/xrfclk-patch)

[xrfdc-patch for PYNQ](https://github.com/Xilinx/RFSoC-MTS/tree/main/boards/patches)


If you have problems with certificates check time and date on your board.
You can set it from the internet with the following command:
```bash
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
```
# Manual build
Fresh WSL2 Ubuntu 20.04 LTS

```bash
# Preparations: or like in https://github.com/nick-petrovsky/PYNQ-ZYBO Readme.md

sudo dpkg --add-architecture i386
sudo apt update

sudo dpkg-reconfigure dash  
Press NO to configure bash

#Install Vivado, Vitis and PetaLinux 2022.1
#Make sure that they are in PATH
export PATH="/opt/crosstool-ng/bin:/opt/qemu/bin:$PATH"
source /work/Vivado/2022.1/settings64.sh
source /work/Vitis/2022.1/settings64.sh
source /work/PetaLinux/2022.1/tool/settings.sh
petalinux-util --webtalk off

#give full rights to pynq directory
sudo chmod -R 777 /work/PYNQ
git checkout 93ddd21

/bin/bash /work/PYNQ/sdbuild/scripts/setup_host.sh

curl -L https://bit.ly/pynq_aarch64_v3_0_1 > pynq_rootfs.aarch64.tar.gz

curl -L https://bit.ly/pynq_arm_v3_1 > pynq_rootfs.arm.tar.gz

curl -L https://files.pythonhosted.org/packages/4c/d4/3a6d15a95d0d6bb47e08f7c3189595f8d20a560560c81de08fb68b624a68/pynq-3.0.1.tar.gz  > pynq_sdist.tar.gz


make images BOARDS=ZCU216 PYNQ_SDIST=/work/PYNQ/sdbuild/prebuilt/pynq_sdist.tar.gz PYNQ_ROOTFS=/work/PYNQ/sdbuild/prebuilt/pynq_rootfs.aarch64.tar.gz
make sysroot_ZCU216 PYNQ_ROOTFS=/work/PYNQ/sdbuild/prebuilt/pynq_rootfs.aarch64.tar.gz

time make BOARDDIR=/home/sega/git-projects/ZCU216-PYNQ/ZCU216/ BOARDS=ZCU216


 source ${HOME}/petalinux/settings.sh
 source /tools/Xilinx/Vivado/2022.1/settings64.sh
 source /tools/Xilinx/Vitis/2022.1/settings64.sh
