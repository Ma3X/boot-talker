# in: osmocom-bb/src/target/firmware
# make cleam
# make mtk-firmware V=1

# make V=1
# make -d
# make 2> warn_err.txt

# arm-none-eabi-gcc -mcpu=arm7tdmi -Iinclude/ -I../../../include -I../../shared/libosmocore/include 
#                   -Wall -Wextra -Wcast-align -Wimplicit -Wunused -Wswitch -Wredundant-decls -Wreturn-type 
#                   -Wshadow -Wnested-externs -Wbad-function-cast -Wsign-compare -Waggregate-return -Os 
#                   -ffunction-sections -gdwarf-2 -DGIT_REVISION=\"osmocon_v0.0.0-1749-gbf83e02-modified\" 
#                   -Wa,-adhlns=lib/vsprintf.lst -c -o lib/vsprintf.o lib/vsprintf.c

# arm-none-eabi-ld -nostartfiles -nostdlib -nodefaultlibs --gc-sections --cref -T board/mediatek/ram.lds 
#                  -Bstatic -Map board/mt62xx/loader_mtk.mtkram.map -o board/mt62xx/loader_mtk.mtkram.elf 
#                  --start-group apps/loader_mtk/main.o flash/cfi_flash.o  board/mediatek/uart.o board/mt62xx/init.o 
#                  board/mediatek/start.ram.o board/mt62xx/loader_mtk.mtkram.manifest.o lib/libmini.a comm/libcomm.a 
#                  ../../shared/libosmocore/build-target/src/.libs/libosmocore.a --end-group

#  $> cd boot-talker/code/hktool/bootload/mediatek
#  $> ln -s ../../../loaders/osmocom-bb/mtk/bins/loader.bin ./mt6253_ram.bin

BASE_DIR=../../../../3rd-party/osmocom-bb/firmwares/mt62xx

DEFP = -std=gnu99 -Wl,-Tlnkscript -Wl,-static -Wl,--gc-sections -nostartfiles -nostdlib -Wl,-Map,vsprintf.map
DEFP = -Wunused -Wswitch -Wredundant-decls -Wreturn-type -Wshadow -Wnested-externs -Wbad-function-cast -Wsign-compare -Waggregate-return -Os
DEFP+= -ffunction-sections -gdwarf-2 -Wa,-adhlns=lib/vsprintf.lst
DEFP+= -Wall -Wextra -Wcast-align -Wimplicit -Wunused -Wswitch -Wredundant-decls -Wreturn-type -DARCH_HAS_CONSOLE
DEFP = -DARCH_HAS_CONSOLE
DEFP = 
DEFS = -DAPPLICATION=\"app\" -DGIT_REVISION=\"git-rev\" -DBOARD=\"brd\" -DENVIRONMENT=\"env\"
CCFLAGS_ASM = -D__ASSEMBLY__
CCFLAGS_INC = -I$(BASE_DIR)/. -I$(BASE_DIR)/../../include
CCFLAGS_WRN = -Wall -Wextra -Wcast-align -Wimplicit -Wunused -Wswitch -Wredundant-decls -Wreturn-type -Wshadow -Wnested-externs -Wbad-function-cast -Wsign-compare -Waggregate-return
CCFLAGS_WRN = 
CCFLAGS_WRN = -Os -ffunction-sections -gdwarf-2
LD_PARAM    = -nostartfiles -nostdlib -nodefaultlibs --gc-sections --cref -Bstatic -Map loader.map
#LD_PARAM    =
OBJS        = objs/main.o objs/init.o objs/uart.o objs/start.ram.o objs/delay.o objs/printf.o \
              objs/ctors.o objs/ctype.o objs/div64.o objs/memcpy.o objs/memset.o \
              objs/lib1funcs.o objs/cfi_flash.o objs/sercomm.o objs/msgb.o objs/console.o \
              objs/string.o objs/crc16.o objs/panic.o objs/l_msgb.o objs/manifest.o \
              objs/vsprintf.o objs/sercomm_cons.o

all:
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/delay.c -o objs/delay.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/printf.c -o objs/printf.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) $(DEFP) -c $(BASE_DIR)/lib/vsprintf.c -o objs/vsprintf.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/ctors.c -o objs/ctors.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/ctype.c -o objs/ctype.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/div64.S -o objs/div64.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_ASM) $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/memcpy.S -o objs/memcpy.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_ASM) $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/memset.S -o objs/memset.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_ASM) $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/lib1funcs.S -o objs/lib1funcs.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/console.c -o objs/console.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/lib/string.c -o objs/string.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/flash/cfi_flash.c -o objs/cfi_flash.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/comm/sercomm.c -o objs/sercomm.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/comm/msgb.c -o objs/msgb.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/comm/sercomm_cons.c -o objs/sercomm_cons.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/libosmocore/crc16.c -o objs/crc16.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -DPANIC_INFLOOP -c $(BASE_DIR)/libosmocore/panic.c -o objs/panic.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c $(BASE_DIR)/libosmocore/msgb.c -o objs/l_msgb.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) $(DEFS) -c $(BASE_DIR)/manifest.c -o objs/manifest.o
	
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c init.c -o objs/init.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c main.c -o objs/main.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c uart.c -o objs/uart.o
	arm-none-eabi-gcc -mcpu=arm7tdmi $(CCFLAGS_INC) $(CCFLAGS_WRN) -c start.ram.S -o objs/start.ram.o
	
	arm-none-eabi-ld $(LD_PARAM) -T ram.lds -o bins/loader.elf --start-group $(OBJS) --end-group
	
	arm-none-eabi-objcopy --gap-fill=0xff -O binary bins/loader.elf bins/loader.bin
	
	arm-none-eabi-size bins/loader.elf | tee bins/loader.size

clean:
	rm -rf objs/*.o
	rm -rf bins/loader.*
