#!/usr/bin/env python
# ert
# gdb -x cs.py
# gdb -q -x cs.py
#                   -q  - Do not print version number on startup
# if console is bla-bla-bla - run: reset

import curses
import curses.textpad
import time
gdb_error = None
try:
  import gdb
except:
  gdb_error = "GDB extension not found!"

def test_1():
    stdscr = curses.initscr()
    
    #curses.noecho()
    #curses.echo()
    
    begin_x = 20
    begin_y = 7
    height = 5
    width = 40
    win = curses.newwin(height, width, begin_y, begin_x)
    tb = curses.textpad.Textbox(win)
    text = tb.edit()
    curses.addstr(4,1,text.encode('utf_8'))
    
    hw = "Hello world!"
    while 1:
        c = stdscr.getch()
        if c == ord('p'):
            break # Exit the while()
        elif c == ord('q'):
            break # Exit the while()
        elif c == curses.KEY_HOME:
            x = y = 0
    
    curses.endwin()

def test_2():
    myscreen = curses.initscr()
    
    myscreen.border(0)
    #myscreen.addstr(12, 25, "Python curses in action!")
    if gdb_error is not None:
        myscreen.addstr(12, 25, gdb_error)
    else:
        myscreen.addstr(12, 25, str("RBX: " + gdb.parse_and_eval("$rbx")) )

    ## Define the topbar menus
    #file_menu = ("File", "file_func()")
    #proxy_menu = ("Proxy Mode", "proxy_func()")
    #doit_menu = ("Do It!", "doit_func()")
    #help_menu = ("Help", "help_func()")
    #exit_menu = ("Exit", "EXIT")
    ## Add the topbar menus to screen object
    #topbar_menu((file_menu, proxy_menu, doit_menu,
    #             help_menu, exit_menu))

    myscreen.refresh()
    myscreen.getch()
    
    curses.endwin()

if __name__=='__main__':
    test_2()
    
    if gdb_error is None:
        gdb.execute('quit')
