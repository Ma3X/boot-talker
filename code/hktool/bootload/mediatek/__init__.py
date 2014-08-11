#!/usr/bin/env python
# -*- coding: utf-8 -*-

#print "MyTool used!"

#from part1 import hello as hello1
#from part2 import hello2

import serial, time, binascii

#--------------------------------------------------------------------

def serialPost(ser, data):
    #time.sleep(0.5)
    #data = chr(0x44)
    print "           -> " + binascii.b2a_hex(data)
    ser.write(data)
    #ser.flush()

def serialPostL(ser, data, slen, scnt):
    sys.stdout.write("\r" + str(scnt) + " of " + str(slen) + " <- " + binascii.b2a_hex(data))
    if slen == scnt: sys.stdout.write("\n")
    #sys.stdout.flush()
    ser.write(data)

def summ(block, length):
    res = 0
    for i in range(length):
      res = res + ord(block[i])
    #print str(res)
    return chr(res & int(0xFF))

def swapSerialData(data):
    l = len(data)
    #if l > 16:
    #    print "-> " + str(l) + " bytes"
    #else:
    #    print "-> " + binascii.b2a_hex(data)
    if len(data) > 0: ser.write(data)
    n = 0
    while n < 1:
      n = ser.inWaiting()
      #time.sleep(1)
    data = ser.read(n)
    l = len(data)
    #print "RX is L: " + str(l) + " -> " + binascii.b2a_hex(data)
    return data
	
#--------------------------------------------------------------------
import threading
from threading import Thread

class Coin():
    ser    = None
    event  = threading.Event()
    last   = None

    def __init__(self, ser):
        #serialPost(ser, "A0".decode("hex"))
        self.ser = ser
        pass

    def run(self):
        while True:
            n = 0
            while n < 1:
                self.event.clear()
                n = self.ser.inWaiting()
            data = self.ser.read(n)
            self.last = data
            leng = len(data)
            print "RX is L: " + str(leng) + " <- " + binascii.b2a_hex(data)
            self.event.set()
        pass

    def onWait(self):
        self.event.wait()
        return self.last

class Cout():
    ser    = None

    def __init__(self, ser):
        self.ser = ser
        pass
    
    # отправка данных в порт с ожиданием ответа
    # self.out.push("A0")
    # wfunc - wait function
    def push(self, data, wfunc):
        serialPost(self.ser, data.decode("hex"))
        return wfunc()
    
    # отправка данных в порт без ожидания ответа
    # self.out("0A")
    #def __call__(self, data):
    def __call__(self, data):
        serialPost(self.ser, data.decode("hex"))

#--------------------------------------------------------------------

# global initial boot commands
x = [
      # initialize bootloading in device
        ["A0",       "0A",       "params" ],
        ["0A",       "A0",       "options"],
        ["50",       "A0",       ""       ],
        ["05",       "A0",       ""       ],
      # get hardware version register
        ["A2",       "A2"      , ""       ],
        ["80010000", "80010000", ""       ],
        ["00000001", "00000001", "+"      ], # 8A02
      # get hardware code register
        ["A2",       "A2"      , ""       ],
        ["80010008", "80010008", ""       ],
        ["00000001", "00000001", "+"      ], # 6253 - mcu is MediaTek MT6253
      # set stop watchdog timer
      # ["A1",       "A1"      , ""       ],
      # ["80030000", "80030000", ""       ],
      # ["00000001", "00000001", ""       ],
      # ["2200",     "2200",     ""       ],
    ]

#class MTKBootload(threading.Thread):
class MTKBootload():
    event  = threading.Event()
    port   = None
    ser    = None
    oin    = None
    out    = None

    def __init__(self, port):
        #threading.Thread.__init__(self)
        self.port = port
        print "x.length: " + str(len(x))
        print "x[0][0]: " + str(x[0][0])
        
        print "serial port: " + self.port
        print "module PySerial version: " + serial.VERSION
        
        self.ser             = serial.Serial()
        self.ser.port        = self.port            # in windows: "2" - "COM3", "COM29", in linux: "/dev/ttyUSB0", "/dev/ttyS0"
        self.ser.baudrate    = 115200               # 9600, 115200, e.t.c.
        self.ser.bytesize    = serial.EIGHTBITS     # number of bits per bytes
        self.ser.parity      = serial.PARITY_EVEN
        self.ser.stopbits    = serial.STOPBITS_ONE  # number of stop bits
        self.ser.timeout     = None                 # block read
        self.ser.rtscts      = True                 # enable hardware (RTS/CTS) flow control (Hardware handshaking)
        
        try:
            self.ser.open()
        except Exception, e:
            print "error open serial port: " + str(e)
            print "for full reset serial device you must reload drivers:"
            print "                                   "
            print "   cat /proc/tty/drivers           "
            print "   lsmod | grep usbserial          "
            print "   sudo modprobe -r pl2303 qcaux   "
            print "   sudo modprobe -r usbserial      "
            print "                                   "
            exit()

        if self.ser.isOpen():
          try:
            print ''
            print 'work with UART port as MediaTek MCU'
            print ''
            self.ser.flushInput()    # flush input buffer, discarding all its contents
            self.ser.flushOutput()   # flush output buffer, aborting current output 
                                # and discard all that is in buffer
            self.check()
          except Exception, e1:
              print "error communicating...: " + str(e1)
              self.ser.close()
              import traceback
              traceback.print_exc()
          except KeyboardInterrupt:
              print "\nmanual interrupted!"
              self.ser.close()
        else:
            print "cannot open serial port "

    def check(self):
        self.oin = Coin(self.ser)
        self.out = Cout(self.ser)

        Thread(target = self.oin.run).start()

        ## initialize bootloading in device
        #res = self.out.push("A0", self.oin.onWait)
        #res = self.out.push("0A", self.oin.onWait)
        #res = self.out.push("50", self.oin.onWait)
        #res = self.out.push("05", self.oin.onWait)
        #
        ## get hardware version register
        #res = self.out.push("A2",       self.oin.onWait)
        #res = self.out.push("80010000", self.oin.onWait)
        #res = self.out.push("00000001", self.oin.onWait)
        #res =                           self.oin.onWait()
        #
        ## set stop watchdog timer
        #res = self.out.push("A1",       self.oin.onWait)
        #res = self.out.push("80030000", self.oin.onWait)
        #res = self.out.push("00000001", self.oin.onWait)
        #res = self.out.push("2200",     self.oin.onWait)

        # general mtk mcu boot code
        for xlist in x:
            res = self.out.push(xlist[0], self.oin.onWait)
            if xlist[2] == '+':
                res = self.oin.onWait()
            if set(xlist) == set(x[-1]):
                mcu = binascii.b2a_hex(res)
                print ''
                print "mcu is: " + mcu
                if mcu == '6253':
                    print "run mcu " + mcu + " boot code"
                    print ''
                    from mt6253 import xboot
                    from mt6253 import xdwag

        # specific mtk mcu boot code
        for xlist in xboot:
            res = self.out.push(xlist[0], self.oin.onWait)
            if xlist[2] == '+':
                res = self.oin.onWait()
                    
        # enter to interactive console
        while True:
            tsk = str(raw_input("enter command > "))
            if tsk.lower() in ['exit', 'quit', 'q']:
                break
            if tsk.lower() in ['get']:
                res = self.oin.onWait()
            if tsk.lower() in ['da', 'downagent']:
                for xlist in xdwag:
                    res = self.out.push(xlist[0], self.oin.onWait)
                    if xlist[2] == '+':
                        res = self.oin.onWait()
                continue
            any = tsk[len(tsk)-1:]
            if any == '+':
                tsk = tsk[:-1]
            res = self.out.push(tsk, self.oin.onWait)
            if any == '+':
                res = self.oin.onWait()
        # "B7" - mtk terminate

        print "Exiting..."
        #mt6253.init(oin, out)
        pass

#--------------------------------------------------------------------

def check(ser):
    mt6253.init()
    pass

def init(port):
    print "serial port: " + port
    print "module PySerial version: " + serial.VERSION
    check(ser)
