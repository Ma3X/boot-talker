/* OUTPUT_FORMAT("binary") */
/* OUTPUT_ARCH(arm)        */
ENTRY(_start)

SECTIONS
{
    . = 0x10000;
    .text : { *(.text) }
}
