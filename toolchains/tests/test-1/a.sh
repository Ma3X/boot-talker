#!/bin/bash

./arm-none-eabi-as -meabi=5 ./a.S -o ./a.o
./arm-none-eabi-ld ./a.o -T ./a.lds -o ./a.elf
./arm-none-eabi-objcopy -O binary ./a.elf ./a.bin
./arm-none-eabi-objdump ./a.elf --disassemble-all > ./a.dis
