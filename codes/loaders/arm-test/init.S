;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@   Bootloader for MT6253
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.equ Mode_USR,   0x10
.equ Mode_FIQ,   0x11
.equ Mode_IRQ,   0x12
.equ Mode_SVC,   0x13
.equ Mode_ABT,   0x17
.equ Mode_UNDEF, 0x1B
.equ Mode_SYS,   0x1F    

.equ SUP_MODE,   0x13                 ;@ Supervisor Mode (SVC)
.equ LOCKOUT,    0xC0                 ;@ Interrupt lockout value
.equ LOCK_MSK,   0xC0                 ;@ Interrupt lockout mask value
.equ MODE_MASK,  0x1F                 ;@ Processor Mode Mask
.equ I_BIT,      0x80                 ;@ Interrupt bit of CPSR and SPSR
.equ F_BIT,      0x40                 ;@ Interrupt bit of CPSR and SPSR
.equ INT_BIT,    0xC0                 ;@ Interrupt bits

.equ SPV_STACK_SIZE, 4096

;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

SPV_Stack_Pool:
   .space SPV_STACK_SIZE
   
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    .text
    .globl INT_Vectors          @ INT_Vectors - глобальный символ, видимый..
                                @ ..за пределами текущего файла

;        .TEXT
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
INT_Vectors:
		b     ResetHandler

Undefined_Handler:
		b     Undefined_Handler

SWIHandler:
		b     SWIHandler

Prefetch_Handler:
		b     Prefetch_Handler

Abort_Handler:
		b     Abort_Handler

Reserved_vector:
		b     Reserved_vector

IrqHandler:
		b     IrqHandler

FiqHandler:
		b     FiqHandler

;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

BOOT_Stack_End:
   .long   SPV_Stack_Pool+SPV_STACK_SIZE-4 

BOOT_Stack_Start:
   .long   SPV_Stack_Pool

;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
ResetHandler:
    ;@ Currently , system is not Remap yet
	
	;@ Turn off I BIT , F BIT
    mrs   r0, CPSR
    orr   r0, r0, #LOCKOUT
    msr   CPSR_cxsf, r0

Start_BootLoader:

    ;@ Chip version check
	
	;@ Initialize stack pointer for Supervisor Mode Stack
	
	;@ initialize stack content as 0xFF

;@  /*
;@   * NoteXXX: EMI initialized program is allocated at internal on MT6238.
;@   *          We must initialize the code segment before initializing EMI.
;@   */

    ;@  Unified Main Body for feature combination
	mov   r2, #0xFFFFFFFF
	ldr   r1, BOOT_Stack_Start
stack_fill_ff:
    cmp   r1, r0          ;@ loop whilst r0 < r1
    str   r2, [r0]
    sub   r0, r0, #4
    blo   stack_fill_ff 

End_BootLoader:
    b     End_BootLoader

Other_Code:	
    teqp  r1, #0xD7
    ldr   sp, =Stackbase1
    teqp  r1, #0xDB
    ldr   sp, =Stackbase2
    teqp  r1, #0xD2
    ldr   sp, =Stackbase3
    teqp  r1, #0xD3
    ldr   sp, =Stackbase4
    ldr   r12, Main_Addr
    bx    r12

Main_Addr:                      ;@ run:
                                ;@> arm-none-eabi-nm main.o
                                ;@ 00000000 T _Z15__program_startv
                                ;@ it is __program_start
        .long program_start
        ;@.long _Z15__program_start
		
Stackbase1:  
        .long 0x808600
Stackbase2:  
        .long 0x808700
Stackbase3:  
        .long 0x808500
Stackbase4:  
        .long 0x807D00
