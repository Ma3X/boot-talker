// forum: VersatilePB board problem PL110 LCD display
// http://www.expertcore.org/viewtopic.php?f=92&t=4375

typedef int(*PFN)(void);

void start(void);


void __attribute__((naked)) entry()
{
   __asm__("mov   sp, #0x60 << 8");
   __asm__("bl   start");
}

#define PL110_CR_EN       0x001
#define PL110_CR_PWR      0x800
#define PL110_IOBASE      0xc0000000
#define PL110_PALBASE    (PL110_IOBASE + 0x200)

typedef unsigned int      uint32;
typedef unsigned char     uint8;
typedef unsigned short    uint16;

typedef struct _PL110MMIO
{
    uint32      volatile tim0;      //  0
    uint32      volatile tim1;      //  4
    uint32      volatile tim2;      //  8
    uint32      volatile d;         //  c
    uint32      volatile upbase;    // 10
    uint32      volatile f;         // 14
    uint32      volatile g;         // 18
    uint32      volatile control;   // 1c
} PL110MMIO;

void start(void)
{
    PFN               fn;
    PL110MMIO        *plio;
    int               x;
    uint16 volatile  *fb;

    plio = (PL110MMIO*)PL110_IOBASE;

    /* 640x480 pixels */
    plio->tim0 = 0x3f1f3f9c;
    plio->tim1 = 0x080b61df;
    plio->upbase = 0x200000;
    /* 16-bit color */
    plio->control = 0x1829;
    fb = (uint16*)0x200000;
    for (x = 0; x < (640 * 480) - 10; ++x)
        fb[x] = 0x1f << (5 + 6) | 0xf << 5;

    /* uncomment this and the function pointer should crash QEMU if you set it for 8MB of ram or less */
    for(;;) ;
    fn = (PFN)0x800f20;
    fn();

    return;
}
