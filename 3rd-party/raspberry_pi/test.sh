#!/bin/bash

#./qemu-system-arm -kernel kernel_rpi_aufs.img -cpu arm1176 -m 512 -M raspi -no-reboot -serial stdio -sd a.img -initrd berryboot.img -append "rw dma.dmachans=0x7f35 bcm2708_fb.fbwidth=1024 bcm2708_fb.fbheight=768 bcm2708.boardrev=0xf bcm2708.serial=0xcad0eedf sdhci-bcm2708.emmc_clock_freq=100000000 vc_mem.mem_base=0x1c000000 vc_mem.mem_size=0x20000000 dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p1 elevator=deadline rootwait" -device usb-kbd -device usb-mouse

./qemu-system-arm -kernel kernel_rpi_aufs.img -cpu arm1176 -m 512 -M raspi -no-reboot -serial stdio -initrd berryboot.img -append "rw dma.dmachans=0x7f35 bcm2708_fb.fbwidth=1024 bcm2708_fb.fbheight=768 bcm2708.boardrev=0xf bcm2708.serial=0xcad0eedf sdhci-bcm2708.emmc_clock_freq=100000000 vc_mem.mem_base=0x1c000000 vc_mem.mem_size=0x20000000 dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p1 elevator=deadline rootwait" -device usb-kbd -device usb-mouse -sd a.img
