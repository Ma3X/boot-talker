# Bare Metal Programming for ARM VersatilePB II : Hello world
# http://imvoid.wordpress.com/2013/05/17/bare-metal-programming-for-arm-versatilepb-hello-world/
# Hello world for bare metal ARM using QEMU
# http://balau82.wordpress.com/2010/02/28/hello-world-for-bare-metal-arm-using-qemu/
# Simplest bare metal program for ARM
# http://balau82.wordpress.com/2010/02/14/simplest-bare-metal-program-for-arm/
#
# use:
#   make
#   make qemu
#
# You can see Hello World Printed in the screen., Now, to close this, Hit,
# 'Ctl + a' and then 'x'

all:
	arm-none-eabi-as -mcpu=arm926ej-s -g startup.s -o startup.o
	arm-none-eabi-gcc -c -mcpu=arm926ej-s -g test.c -o test.o
	arm-none-eabi-ld -T test.ld test.o startup.o -o test.elf
	arm-none-eabi-objcopy -O binary test.elf test.bin

qemu: all
	@echo
	@echo Now, to close this, hit: \'Ctl + a\' and then \'x\'
	@echo
	qemu-system-arm -M versatilepb -m 128M -nographic -kernel test.bin

clean:
	rm -rf *.o *.elf *.bin
