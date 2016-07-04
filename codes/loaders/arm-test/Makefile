# build all default targets
all:
		arm-none-eabi-as -o init.o init.S
		arm-none-eabi-gcc -c -nostdlib -fomit-frame-pointer -O3 -o main.o main.c
		arm-none-eabi-ld -T memmap.lds -o init.elf init.o main.o
#		arm-none-eabi-strip init.elf
#		arm-none-eabi-as init.S
#		arm-none-eabi-gcc main.c
#		arm-none-eabi-ld
#       arm-none-eabi-g++ -c -nostdlib -fomit-frame-pointer -O3 -S main.c
#       arm-none-eabi-g++ -c -nostdlib -fomit-frame-pointer -O2 -S main.c

# test section or memory structure
test: all
		arm-none-eabi-nm -n init.elf

to-hex: all
		arm-none-eabi-objcopy -O ihex init.elf init.hex

to-bin: all
		arm-none-eabi-objcopy -O binary init.elf init.bin

clean:
		rm -f *.o *.elf *.hex *.bin main.s
