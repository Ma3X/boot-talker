#!/usr/bin/env python
# -*- coding: utf-8 -*-

#print "MyTool used!"

#from part1 import hello as hello1
#from part2 import hello2

import serial, time, binascii
import os

#--------------------------------------------------------------------

def serialPost(ser, data):
    #time.sleep(0.5)
    #data = chr(0x44)
    print "           -> " + binascii.b2a_hex(data)
    ser.write(data)
    #ser.flush()

def serialPostBin(ser, data):
    #time.sleep(0.5)
    #data = chr(0x44)
    #print "           -> " + binascii.b2a_hex(data)
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
    cond   = threading.Condition()
    last   = None

    def __init__(self, ser):
        #serialPost(ser, "A0".decode("hex"))
        self.ser = ser
        pass

    #@staticmethod
    def run(self):
        u"""A decorator function to implement a blocking method on a thread"""
        while True:
            n = 0
            while n < 1:
                self.event.clear()
                #self.cond.acquire()
                n = self.ser.inWaiting()
            data = self.ser.read(n)
            self.last = data
            leng = len(data)
            print "RX is L: " + str(leng) + " <- " + binascii.b2a_hex(data)
            self.event.set()
            #self.cond.notifyAll()
            ##self.cond.release()
        pass

    #@staticmethod
    def onWait(self):
        u"""A decorator function to implement a non-blocking method on a
        thread
        """
        self.event.wait()
        #self.cond.acquire()
        #try:
        #  self.cond.wait(timeout=2)
        #except RuntimeError:
        #  print "Time is out!"
        #finally:
        #  self.cond.release()
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

    def push_bin(self, data, wfunc):
        serialPostBin(self.ser, data)
        return wfunc()
    
    # отправка данных в порт без ожидания ответа
    # self.out("0A")
    #def __call__(self, data):
    def __call__(self, data):
        serialPost(self.ser, data.decode("hex"))

    def call_bin(self, data):
        serialPostBin(self.ser, data)

#--------------------------------------------------------------------

# global initial boot commands
x = [
      # initialize bootloading in device
        ["A0",       "5F",       "params" ],
        ["0A",       "F5",       "options"],
        ["50",       "AF",       ""       ],
        ["05",       "FA",       ""       ],
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
        try:
          for xlist in x:
            res = self.out.push(xlist[0], self.oin.onWait)
            #resS= binascii.b2a_hex(res)
            #print "resS: " + resS
            #if xlist[2] == 'params':
            #    print "doubling..."
            #    if resS.lower() <> xlist[1].lower():
            #        res = self.out.push(xlist[0], self.oin.onWait)
            if xlist[2] == '+':
                res = self.oin.onWait()
            #if set(xlist) == set(x[-1]):
            #    mcu = binascii.b2a_hex(res)
            #    print ''
            #    print "mcu is: " + mcu
            #    if mcu == '6253':
            #        print "run mcu " + mcu + " boot code"
            #        print ''
            #        from mt6253 import xboot
            #        from mt6253 import xdwag
            #        from hktool.bootload.mediatek import mt6253 as mtk_spec
            #    if mcu == '6235':
            #        print "run mcu " + mcu + " boot code"
            #        print ''
            #        from mt6235 import xboot
            #        from mt6235 import xdwag
            #        from hktool.bootload.mediatek import mt6235 as mtk_spec
        except SerialException, e1:
            print "error communicating...: " + str(e1)
            self.ser.close()
            import traceback
            traceback.print_exc()
            print "Exiting..."
            os._exit(0)

        # specific mtk mcu boot code
        for xlist in xboot:
            res = self.out.push(xlist[0], self.oin.onWait)
            if xlist[2] == '+':
                res = self.oin.onWait()
                    
        # enter to interactive console
        while True:
            tsk = str(raw_input("enter command > "))
            # exit from loop
            if tsk.lower() in ['exit', 'quit', 'q']:
                break
            # checksum logical XOR tester
            if tsk.lower() in ['crc']:
                #str1 = raw_input("Enter one hex word: ")
                #str2 = raw_input("Enter two hex word: ")
                #print hex(int(str1, 16) ^ int(str2, 16))
                #print "XOR-ed words is: " + words_xor(str1.decode('hex'))
                #from ...common.logical import words_xor, word_byteswap, chunkstring
                from ...common import logical
                from mt6253 import load_bootcode_first as mtk_first_bootcode
                loader1 = mtk_first_bootcode()
                print "loader data size is: " + str(len(loader1))
                ldr1_sz = len(loader1)
                ldr1_swp = logical.word_byteswap(loader1)       # loader1[s:s-1]
                ldr1_cnk = logical.chunkstring(ldr1_swp, 1024)
                j = 0
                #for i in ldr1_cnk:
                #    j += 1
                #    print str(j) + " -> " + str(len(i))
                print "loader1 XOR-ed checksum is: " + binascii.b2a_hex(logical.words_xor(ldr1_swp))
                continue
            # force wait
            if tsk.lower() in ['get']:
                res = self.oin.onWait()
            # exec downagent code
            if tsk.lower() in ['da', 'downagent']:
                from mt6253 import xdwag
                last_wait_bytes = 0
                for xlist in xdwag:
                    res = self.out.push(xlist[0], self.oin.onWait)
                    last_wait_bytes = len(xlist[1].decode('hex'))
                    if xlist[2] == '+' and last_wait_bytes <= self.oin.last:
                        res = self.oin.onWait()
                continue
            if tsk.lower() in ['test', 't']:
                #from hktool.bootload.mediatek import mt6235
                reload(mtk_spec)
                loader1 = mtk_spec.load_bootcode_first()
                ldr1_sz = len(loader1)
                print "loader data size is: " + str(ldr1_sz)
                from ...common import logical
                ldr1_swp = logical.word_byteswap(loader1)       # loader1[s:s-1]
                ldr1_crc = logical.words_xor(ldr1_swp)
                print "loader1 XOR-ed checksum is: " + binascii.b2a_hex(ldr1_crc)
                ldr1_cnk = logical.chunkstring(ldr1_swp, 1024)
                mtk_spec.test_boot(self.out, self.oin, ldr1_cnk, ldr1_crc)
                continue
            # other code for base task
            any = tsk[len(tsk)-1:]
            if any == '+':
                tsk = tsk[:-1]
            res = self.out.push(tsk, self.oin.onWait)
            if any == '+':
                res = self.oin.onWait()
        # "B7" - mtk terminate

        print "Exiting..."
        os._exit(0)
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
