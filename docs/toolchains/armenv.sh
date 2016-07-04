# download toolchain from:
#   https://sourcery.mentor.com/GNUToolchain/subscription3053?lite=arm&lite=ARM&signature=4-1330864567-0-e3ad3089427f58b2a4a8bdf30f5fb0fb4ae5e79f
#  Sourcery CodeBench Lite 2013.11-24
#   https://sourcery.mentor.com/GNUToolchain/release2635
#   https://sourcery.mentor.com/GNUToolchain/package12190/public/arm-none-eabi/arm-2013.11-24-arm-none-eabi-i686-pc-linux-gnu.tar.bz2
#
# make -C target/firmware CROSS_COMPILE=arm-none-eabi-
# make CROSS_COMPILE=arm-none-eabi- -f Makefile.test
# make CROSS_COMPILE=arm-none-eabi- -f Makefile.test.mtk
# make mtk-loader
# make -d CROSS_COMPILE=arm-none-eabi- -f Makefile.test.mtk > a
# ./osmocon -p /dev/ttyUSB0 -m mtk ../../target/firmware/board/mt62xx/loader.mtkram.bin
# ./osmocon -p /dev/ttyUSB0 -m mtk ./loader_mtk.mtkram.bin

CROSS_COMPILE=arm-none-eabi-
PATH=/home/nouser/mobile/arm-2013.11/bin:$PATH
#PATH=/mnt/sda2/mobile/arm-2013.11/bin:$PATH
