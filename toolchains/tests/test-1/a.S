.global _start

_start:
    bl function

function:
    stmdb sp!, {r4-r11}
