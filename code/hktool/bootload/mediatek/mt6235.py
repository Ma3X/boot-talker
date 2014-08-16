#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------
import signal
import sys
import os

def mt_signal_handler(signal, frame):
    global gout, goin
    print '\nYou pressed Ctrl+C!'
    goin.event.set()
    time.sleep(0.1)
    goin.event.clear()

#signal.signal(signal.SIGINT, signal_handler)

def catcher(signum, _):
    global gout, goin
    print '\ntime is out!'
    goin.event.set()
    time.sleep(0.1)
    goin.event.clear()

#-------------------------------------------------------------------------------------
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_bootcode_first():
  return open(os.path.join(__location__, "mt6235.bin"), "rb").read()

xboot = [
          # initialize bootloading in device
          # ["A0",       "0A",       "params" ],
          # ["0A",       "A0",       "options"],
          # ["50",       "A0",       ""       ],
          # ["05",       "A0",       ""       ],
          # get hardware version register
          # ["A2",       "A2"      , ""       ],
          # ["80010000", "80010000", ""       ],
          # ["00000001", "00000001", "+"      ], # 8A02
          # get hardware code register
          # ["A2",       "A2"      , ""       ],
          # ["80010008", "80010008", ""       ],
          # ["00000001", "00000001", "+"      ], # 6253 - mcu is MediaTek MT6253
          # set stop watchdog timer
            ["A1",       "A1"      , ""       ],
            ["80030000", "80030000", ""       ],
            ["00000001", "00000001", ""       ],
            ["2200",     "2200",     ""       ],
        ]

xdwag = [ # loading Download Agent
          # get RTC
            ["A2",       "A2"      , ""       ],
            ["810C0050", "810C0050", ""       ],
            ["00000001", "00000001", "+"      ], # A357
          # get RTC
            ["A2",       "A2"      , ""       ],
            ["810C0054", "810C0054", ""       ],
            ["00000001", "00000001", "+"      ], # 67D2
        ]

tboot = [
            ["A2",       "A2"      , ""       ],
            ["80000000", "80000000", ""       ],
            ["00000001", "00000001", "+"      ],
            ["A2",       "A2"      , ""       ],
            ["80010008", "80010008", ""       ],
            ["00000001", "00000001", "+"      ], # 6235
            ["A2",       "A2"      , ""       ],
            ["00000000", "00000000", ""       ],
            ["00000001", "00000001", "+"      ],
            ["A4",       "A4"      , ""       ],
            ["00000000", "00000000", ""       ],
            ["00000001", "00000001", "+"      ],
        ]

class TimeLimitExpired(Exception): pass

def timelimit(timeout, func, args=(), kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """
    import threading
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(*args, **kwargs)

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        raise TimeLimitExpired()
    else:
        return it.result
        
def test_boot(out, oin, cnk, crc):
    global gout, goin
    gout = out
    goin = oin
    #signal.signal(signal.SIGINT, mt_signal_handler)
    #signal.signal(signal.CTRL_C_EVENT, mt_signal_handler)

    last_wait_bytes = 0
    for xlist in tboot:
        res = out.push(xlist[0], oin.onWait)
        last_wait_bytes = len(xlist[1].decode('hex'))
        last_oin_len    = len(oin.last)
        #print "xlist[2]: " + str(xlist[2]) + " - " + "last_wait_bytes -> " + str(last_wait_bytes) + " : " + str(last_oin_len) + " <- oin.last"
        if xlist[2] == '+' and last_wait_bytes >= last_oin_len:
            #signal.signal(signal.SIGALRM, catcher)
            #signal.setitimer(signal.ITIMER_REAL, 2, 2)
            #res = oin.onWait()
            try:
              timelimit(1, oin.onWait, args=(), kwargs={})
            except TimeLimitExpired:
              #print "Time is out!"
              print " - "
            #signal.setitimer(signal.ITIMER_REAL, 0)
            
    #signal.signal(signal.CTRL_C_EVENT, signal.SIG_DFL)
    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    pass
    while True:
        res = out.push("AD",       oin.onWait)
        res = out.push("40000000", oin.onWait)
        res = out.push("000021DA", oin.onWait)  # 43 B4 / 2 = 21 DA
        j = 0
        for i in cnk:
            j += 1
            res = out.call_bin(i)
            print str(j) + " -> " + str(len(i))
            import time
            time.sleep(0.1)
        res = out.push("A4",       oin.onWait)
        res = out.push("40000000", oin.onWait)
        res = out.push("000021DA", oin.onWait)  # -> E3 62  (1024*16 + 948)
        try:
            timelimit(1, oin.onWait, args=(), kwargs={})
        except TimeLimitExpired:
            print " - "
        #res = out.push("A8",       oin.onWait)
        #res = out.push("40000000", oin.onWait)  # jump to 0x40000000
        #try:
        #    timelimit(1, oin.onWait, args=(), kwargs={})
        #except TimeLimitExpired:
        #    print " - "
        break
    while False:
        print "Working with lxml..."
        print ""
        from lxml import etree
        tree = etree.parse('../../mtk-tests/Projects/_texet-tm510r/data/UTLog_memtest.xml')
        root = tree.getroot()
        print root
        #entries = tree.xpath("//atom:category[@term='accessibility']/..", namespaces=NSMAP)
        entries = tree.xpath("//UTLOG/Request[@Dir='[OUT]']/Data")
        #print entries
        old_text = None
        dmp_text = False
        cnt_text = 0
        bin_file = None
        for xent in entries:
            new_text = xent.text
            
            if new_text == old_text:
                continue
            old_text = new_text
            #print "-> " + new_text
            
            bin_text = new_text.replace(" ", "")
            bin_text = bin_text.decode("hex")
            bin_len  = len(bin_text)
            #print str(bin_len) + " -> " + new_text
            if dmp_text is False and bin_len == 1024:
                dmp_text = True
                prt = xent.getparent()
                atr = prt.attrib
                num = atr["Number"]
                nam = "big_" + num + ".bin"
                bin_file = open(nam, 'wb')
                print ""
                print "start dump big data to: " + nam
            if dmp_text is True:
                #---
                import array
                a = array.array('H', bin_text)  # array.array('H', bin_text)
                a.byteswap()
                bin_text = a.tostring()
                #---
                bin_file.write(bin_text)
                if bin_len == 1024:
                    cnt_text += 1
                else:
                    cnt_text = cnt_text * 1024 + bin_len
                    dmp_text = False
                    bin_file.close()
                    print "big data length is: " + str(cnt_text)
                    print ""
                    cnt_text = 0
        break
    pass
