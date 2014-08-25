# in: osmocom-bb/src/target/firmware
# make cleam
# make mtk-firmware V=1

# make V=1
# make -d
# make 2> warn_err.txt

DEFS=-DAPPLICATION="app" -DGIT_REVISION="git-rev" -DBOARD="brd" -DENVIRONMENT="env"
CCFLAGS_ASM = -D__ASSEMBLY__
CCFLAGS_INC = -I. -I../../include
CCFLAGS_WRN = -Wall -Wextra -Wcast-align -Wimplicit -Wunused -Wswitch -Wredundant-decls -Wreturn-type -Wshadow -Wnested-externs -Wbad-function-cast -Wsign-compare -Waggregate-return
CCFLAGS_WRN = 

all:
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/delay.c -o objs/delay.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/printf.c -o objs/printf.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -Wl,-Tlnkscript -Wl,-static -Wl,--gc-sections -nostartfiles -nostdlib -Wl,-Map,vsprintf.map -c lib/vsprintf.c -o objs/vsprintf.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/ctors.c -o objs/ctors.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/ctype.c -o objs/ctype.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/div64.S -o objs/div64.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_ASM) $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/memcpy.S -o objs/memcpy.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_ASM) $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/memset.S -o objs/memset.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_ASM) $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/lib1funcs.S -o objs/lib1funcs.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/console.c -o objs/console.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c lib/string.c -o objs/string.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c flash/cfi_flash.c -o objs/cfi_flash.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c comm/sercomm.c -o objs/sercomm.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c comm/msgb.c -o objs/msgb.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c libosmocore/crc16.c -o objs/crc16.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -DPANIC_INFLOOP -c libosmocore/panic.c -o objs/panic.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c libosmocore/msgb.c -o objs/l_msgb.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) $(DEFS) -c manifest.c -o objs/manifest.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_WRN) -c init.c -o objs/init.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_WRN) -c main.c -o objs/main.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_WRN) -c uart.c -o objs/uart.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_WRN) -c start.ram.S -o objs/start.ram.o
	arm-none-eabi-ld -T ram.lds -o loader.elf objs/main.o objs/init.o objs/uart.o objs/start.ram.o objs/delay.o objs/printf.o \
                                                  objs/ctors.o objs/ctype.o objs/div64.o objs/memcpy.o objs/memset.o \
                                                  objs/lib1funcs.o objs/cfi_flash.o objs/sercomm.o objs/msgb.o objs/console.o \
                                                  objs/string.o objs/crc16.o objs/panic.o objs/l_msgb.o objs/manifest.o \
                                                  objs/vsprintf.o
