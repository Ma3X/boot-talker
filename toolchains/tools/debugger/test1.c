#include <ncurses.h> // подключаем библиотеку ncurses
//#include <curses.h>

void out_no_color()
{
  move( 1,  0); printw("-----------------------");
  move( 2,  0); printw("gdb    path: /home/user/temt/toolchain-2009q3/bin/arm-noeabi-gdb");
  move( 3,  0); printw("gdb version: 4.7.1 (i686, target: arm-noeabi)");
  move( 4,  0); printw("Current CPU: Amlogic Meson3 (aml8726-mx)");
  move( 5,  0); printw("=======================================================================================");
  move( 6,  0); printw("source file: /usr/src/linux/arch/arm/boot/init.S");
  move( 7,  0); printw("---------------------------------------------------------------------------------------");
  move( 8,  0);
  move( 9,  0); printw("_start:");
  move(10,  0); printw("    21 43 54 65    add     lr, pc, #-0x8           @ lr = current load addr");
  move(11,  0); printw("    65 76          adr     r13, data");
  move(12,  0); printw("    54 23          ldmia   r13!, {r4-r6}           @ r5 = dest, r6 = length");
  move(13,  0); printw("    23 56          add     r4, r4, lr              @ r4 = initrd_start + load addr");
  move(14,  0); printw("    45 56 67 78    bl      move                    @ move the initrd");
  move(15,  0); printw("");
  move(16,  0); printw("/*");
  move(17,  0); printw(" * Setup the initrd parameters to pass to the kernel.  This can only be");
  move(18,  0); printw(" * passed in via the tagged list.");
  move(19,  0); printw(" */");
  move(20,  0); printw("    45 56 67 78    ldmia   r13, {r5-r9}            @ get size and addr of initrd");
  move(21,  0); printw("                                                   @ r5 = ATAG_CORE");
  move(22,  0); printw("                                                   @ r6 = ATAG_INITRD2");
  move(23,  0); printw("                                                   @ r7 = initrd start");
  move(24,  0); printw("                                                   @ r8 = initrd end");
  move(25,  0); printw("                                                   @ r9 = param_struct address");
  move(26,  0); printw("");
  move(27,  0); printw("    56 67          ldr     r10, [r9, #4]           @ get first tag");
  move(28,  0); printw("    54 32          teq     r10, r5                 @ is it ATAG_CORE?");
  move(29,  0);
  move(30,  0); printw("=======================================================================================");

  move( 0, 87); printw("| r0:   0x12345678 |");
  move( 1, 87); printw("| r1:   0x12345678 |");
  move( 2, 87); printw("| r2:   0x12345678 |");
  move( 3, 87); printw("| r3:   0x12345678 |");
  move( 4, 87); printw("| r4:   0x12345678 |");
  move( 5, 87); printw("| r5:   0x12345678 |");
  move( 6, 87); printw("| r6:   0x12345678 |");
  move( 7, 87); printw("| r7:   0x12345678 |");
  move( 8, 87); printw("|------------------|");
  move( 9, 87); printw("| r8:   0x12345678 |");
  move(10, 87); printw("| r9:   0x12345678 |");
  move(11, 87); printw("| r10:  0x12345678 |");
  move(12, 87); printw("| r11:  0x12345678 |");
  move(13, 87); printw("| r12:  0x12345678 |");
  move(14, 87); printw("|------------------|");
  move(15, 87); printw("| r13:  0x12345678 |");
  move(16, 87); printw("| r14:  0x12345678 |");
  move(17, 87); printw("| r15:  0x12345678 |");
  move(18, 87); printw("|------------------|");
  move(19, 87); printw("| cpsr: ********** |");
  move(20, 87); printw("| spsr: ********** |");
  move(21, 87); printw("|------------------|");
  move(22, 87); printw("|                  |");
  move(23, 87); printw("|                  |");
  move(24, 87); printw("|                  |");
  move(25, 87); printw("|                  |");
  move(26, 87); printw("|                  |");
  move(27, 87); printw("|                  |");
  move(28, 87); printw("|                  |");
  move(29, 87); printw("|                  |");
  move(30, 87); printw("====================");
}

void out_color()
{
  move( 1,  0); printw("-----------------------");
  move( 2,  0);
    attron(COLOR_PAIR(1));
    printw("gdb    path: ");
    attron(COLOR_PAIR(3));
    printw("/home/user/temt/toolchain-2009q3/bin/arm-noeabi-gdb");
    attrset(A_NORMAL);
  move( 3,  0);
    attron(COLOR_PAIR(1));
    printw("gdb version: ");
    attron(COLOR_PAIR(3));
    printw("4.7.1 (i686, target: arm-noeabi)");
    attrset(A_NORMAL);
  move( 4,  0);
    attron(COLOR_PAIR(1));
    printw("Current CPU: ");
    attron(COLOR_PAIR(3));
    printw("Amlogic Meson3 (aml8726-mx)");
    attrset(A_NORMAL);
  move( 5,  0); printw("=======================================================================================");
  move( 6,  0); printw("source file: /usr/src/linux/arch/arm/boot/init.S");
  move( 7,  0); printw("---------------------------------------------------------------------------------------");
  move( 8,  0);
  move( 9,  0); printw("_start:");
  move(10,  0); printw("00000000    21 43 54 65    add     lr, pc, #-0x8       @ lr = current load addr");
  move(11,  0); printw("      +4    65 76          adr     r13, data");
  move(12,  0); printw("      +6    54 23          ldmia   r13!, {r4-r6}       @ r5 = dest, r6 = length");
  move(13,  0); printw("      +8    23 56          add     r4, r4, lr          @ r4 = initrd_start + load addr ");
  move(14,  0); printw("      +A    45 56 67 78    bl      move                @ move the initrd");
  move(15,  0); printw("");
  move(16,  0); printw("/*");
  move(17,  0); printw(" * Setup the initrd parameters to pass to the kernel.  This can only be");
  move(18,  0); printw(" * passed in via the tagged list.");
  move(19,  0); printw(" */");
  move(20,  0); printw("0000000E    45 56 67 78    ldmia   r13, {r5-r9}        @ get size and addr of initrd");
  move(21,  0); printw("                                                       @ r5 = ATAG_CORE");
  move(22,  0); printw("                                                       @ r6 = ATAG_INITRD2");
  move(23,  0); printw("                                                       @ r7 = initrd start");
  move(24,  0); printw("                                                       @ r8 = initrd end");
  move(25,  0); printw("                                                       @ r9 = param_struct address");
  move(26,  0); printw("");
  move(27,  0); printw("00000012    56 67          ldr     r10, [r9, #4]       @ get first tag");
  move(28,  0); printw("     +14    54 32          teq     r10, r5             @ is it ATAG_CORE?");
  move(29,  0);
  move(30,  0); printw("=======================================================================================");

  move( 0, 87); printw("| r0:   0x12345678 |");
  move( 1, 87); printw("| r1:   0x12345678 |");
  move( 2, 87); printw("| r2:   0x12345678 |");
  move( 3, 87); printw("| r3:   0x12345678 |");
  move( 4, 87); printw("| r4:   0x12345678 |");
  move( 5, 87); printw("| r5:   0x12345678 |");
  move( 6, 87); printw("| r6:   0x12345678 |");
  move( 7, 87); printw("| r7:   0x12345678 |");
  move( 8, 87); printw("|------------------|");
  move( 9, 87); printw("| r8:   0x12345678 |");
  move(10, 87); printw("| r9:   0x12345678 |");
  move(11, 87); printw("| r10:  0x12345678 |");
  move(12, 87); printw("| r11:  0x12345678 |");
  move(13, 87); printw("| r12:  0x12345678 |");
  move(14, 87); printw("|------------------|");
  move(15, 87); printw("| r13:  0x12345678 |");
  move(16, 87); printw("| r14:  0x12345678 |");
  move(17, 87); printw("| r15:  0x12345678 |");
  move(18, 87); printw("|------------------|");
  move(19, 87); printw("| cpsr: ********** |");
  move(20, 87); printw("| spsr: ********** |");
  move(21, 87); printw("|------------------|");
  move(22, 87); printw("|                  |");
  move(23, 87); printw("|                  |");
  move(24, 87); printw("|                  |");
  move(25, 87); printw("|                  |");
  move(26, 87); printw("|                  |");
  move(27, 87); printw("|                  |");
  move(28, 87); printw("|                  |");
  move(29, 87); printw("|                  |");
  move(30, 87); printw("====================");
}

int main(int argc, char* argv[])
{
  // инициализация (должна быть выполнена перед использованием ncurses)
  initscr();

  // перемещение курсора в стандартном экране y=10 x=30
  //move(10, 30);


  move( 0,  0); printw("Welcome to ARM Debugger"); //if (has_colors()) printw(" (with colors support)");

  if (!has_colors())
  {
    endwin();
    //printf("Цвета не поддерживаются");
    //exit(1);

    out_no_color();

  } else {
    start_color();

    // 1 цвет в палитре - красные символы на чёрном фоне
    init_pair(1, COLOR_RED, COLOR_BLACK);

    // 2 цвет в палитре - зелёные символы на желтом фоне
    init_pair(2, COLOR_GREEN, COLOR_YELLOW);

    init_pair(3, COLOR_GREEN, COLOR_BLACK);

    if (has_colors()) printw(" (with colors support)");
    out_color();
  }

  move(31,  0); printw(":");
  chtype ch = '_' | A_BLINK;
  //insch(ch);
  addch(ch);
  ch = '*' | A_BOLD;        // - повышенная яркость
  addch(ch);
  ch = '*' | A_DIM;         // - пониженная яркость
  addch(ch);
  ch = '*' | A_NORMAL;      // - нормальное отображение
  addch(ch);
  ch = '*' | A_UNDERLINE;   // - подчёркнутый
  addch(ch);
  ch = '*' | A_REVERSE;     // - инверсный
  addch(ch);
  ch = '*' | COLOR_PAIR(1); // символ с цветом 1 из палитры
  addch(ch);
  ch = '*' | COLOR_PAIR(1) | A_BOLD;
  addch(ch);

  //printw("Hello world !!!"); // вывод строки
  refresh(); // обновить

  int key = 0;
  //WINDOW *window;
  //c = wgetch(window);
  keypad(stdscr, TRUE);
  while( (key = wgetch(stdscr)) != KEY_F(10) )
  {
    switch(key)
    {
      case KEY_F(1):
        printw("Help");
        break;
      default:
        printw("Unknown");
        break;
    }
    refresh();
  }

  //getch();   // ждем нажатия символа

  endwin();  // завершение работы с ncurses
}
