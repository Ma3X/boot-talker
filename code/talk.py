#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG    = True
observer = None
ser_port = None
s        = 0
ser      = None

#--------------------------------------------------------------------
import signal
import sys
import os

def signal_handler(signal, frame):
    global s, ser
    print '\nYou pressed Ctrl+C!'
    if s > 18:
      print "MTK_Finalize"
      serialPost(ser, "B7".decode("hex"))
      time.sleep(0.1)
    if ser.isOpen(): ser.close()
    #sys.exit(0)
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

#--------------------------------------------------------------------
import os
import serial
from serial.tools import list_ports

def serial_ports():
    """
    Returns a generator for all available serial ports
    """
    if os.name == 'nt':
     # windows
     for i in range(256):
      try:
        s = serial.Serial(i)
        s.close()
        yield 'COM' + str(i + 1)
      except serial.SerialException:
        pass
    else:
     # unix
     for port in list_ports.comports():
        yield port[0]


#if __name__ == '__main__':
#    print(list(serial_ports()))

#exit()
    
#--------------------------------------------------------------------

import serial, time, binascii

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

#----- CONNECT TO PORT----------
def conn_port (ser_port):
  print ser_port
  print "module PySerial version: " + serial.VERSION

  # if: error open serial port: (22, 'Invalid argument')
  # http://superuser.com/questions/572034/how-to-restart-ttyusb
  # cat /proc/tty/drivers
  # lsmod | grep usbserial
  # sudo modprobe -r pl2303 qcaux
  # sudo modprobe -r usbserial

  #import subprocess
  #subprocess.call(['statserial', ser_port])
  #subprocess.call(['setserial',  '-G', ser_port])

  # http://www.roman10.net/serial-port-communication-in-python/
  # initialization and open the port
  # possible timeout values:
  #    1. None: wait forever, block call
  #    2. 0: non-blocking mode, return immediately
  #    3. x, x is bigger than 0, float allowed, timeout block call

  global ser
  ser         = serial.Serial()
  #ser.port   = "COM29"
  ser.port    = ser_port
  ser.baudrate    = 115200
  ser.bytesize    = serial.EIGHTBITS     # number of bits per bytes
  ser.parity      = serial.PARITY_EVEN
  ser.stopbits    = serial.STOPBITS_ONE  # number of stop bits
  ser.timeout     = None         # block read
  ser.rtscts      = True         # enable hardware (RTS/CTS) flow control (Hardware handshaking)

  #ser.port   = "/dev/ttyS0"
  #ser.port   = "/dev/ttyUSB0"
  #ser.port   = "2"          # COM3
  #ser.baudrate   = 9600
  #ser.parity     = serial.PARITY_NONE   # set parity check: no parity
  #ser.timeout    = 0            # non-block read
  #ser.xonxoff    = False        # disable software flow control
  #ser.rtscts     = False        # disable hardware (RTS/CTS) flow control
  #ser.dsrdtr     = False        # disable hardware (DSR/DTR) flow control
  #ser.writeTimeout = 2          # timeout for write

  #data = chr(0x44) + chr(0x59)
  #print "-> " + binascii.b2a_hex(data)
  #exit()

  try:
    ser.open()

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

  from hktool.bootload.samsung import sgh_e730

  #loader1 = open("loader1.bin", "rb").read()
  loader1 = sgh_e730.load_bootcode_first()
  print "loader1.bin data size is: " + str(len(loader1))
  ldr1_i = 0
  ldr1_l = len(loader1)
  ldr1_c = "4c00".decode("hex")

  #loader2 = open("loader2.bin", "rb").read()
  loader2 = sgh_e730.load_bootcode_second()
  print "loader2.bin data size is: " + str(len(loader2))
  ldr2_i = 0
  ldr2_l = len(loader2)

  #f = open("loader1.bin", "rb")
  #try:
  #    byte = f.read(1)
  #    while byte != "":
  #  # Do stuff with byte.
  #  byte = f.read(1)
  #except Exception, e1:
  #    print "error: " + str(e1)
  #    ser.close()
  #    import traceback
  #    traceback.print_exc()
  #finally:
  #    f.close()

  global s
  if ser.isOpen():
   try:
    print 'Work with Samsung SGH-E730:'
    print '- wait for SWIFT power on...'
    
    ser.flushInput()   # flush input buffer, discarding all its contents
    ser.flushOutput()  # flush output buffer, aborting current output 
               # and discard all that is in buffer
    # write data
    #ser.write("AT+CSQ=?\x0D")
    #print("write data: AT+CSQ=?\x0D")
    
    # steps
    s = 0
    serialPost(ser, "A0".decode("hex"))
    while True:
        n = 0
        s += 1
        while n < 1:
          n = ser.inWaiting()
          #time.sleep(1)
        data = ser.read(n)
        l = len(data)
        #if s != 6 or ldr1_i == 0:
        print "RX is L: " + str(l) + " <- " + binascii.b2a_hex(data)
        if s == 1:
          if data[l-1] == chr(0x5F):
            serialPost(ser, chr(0x0A))
        elif s == 2:
          if data[l-1] == chr(0xF5):
            serialPost(ser, chr(0x50))
        elif s == 3:
          #if l == 16:
          # serialPost(ser, "4412345678".decode("hex") + data)
          # -> AF
          serialPost(ser, "05".decode("hex"))
        elif s == 4:
          #if data[l-1] == chr(0x4f):
          # # set timeout to 1600 ms (10h)
          # serialPost(ser, chr(0x54) + chr(0x10))
          # # set timeout to 1600 ms (20h)
          # #serialPost(ser, chr(0x54) + chr(0x20))
          # -> FA
          # A2 - read from memory
          serialPost(ser, "A2".decode("hex"))
        elif s == 5:
          #if data[l-1] == chr(0x4f):
          # serialPost(ser, "530000000c".decode("hex"))
          # -> A2       - read command ACK
          # 80 01 00 00 - Configuration Register: Hardware Version Register
          serialPost(ser, "80010000".decode("hex"))
        elif s == 6:
          # -> 80 01 00 00
          # 00 00 00 01 - read one byte
          serialPost(ser, "00000001".decode("hex"))
          #ldr1_i4 = 4*ldr1_i
          #ldr1_i8 = 4*ldr1_i + 4
          #if ldr1_i8 < ldr1_l:
          # serialPostL(ser, ldr1_c + loader1[ldr1_i4:ldr1_i8], ldr1_l, ldr1_i8)
          # s -= 1
          #else:
          # serialPostL(ser, ldr1_c + loader1[ldr1_i4:ldr1_l ], ldr1_l, ldr1_l )
          #ldr1_i += 1
        elif s == 7:
          if l == 6: s += 1
        elif s == 8:
          # -> 00 00 00 01  - byte is read
          # -> XX XX        - byte: 
          serialPost(ser, "A2".decode("hex"))
          #if data[l-1] == chr(0x4f):
          # serialPost(ser, "530000000c".decode("hex"))
        elif s == 9:
          # -> A2
          # 80 01 00 08 - Hardware Code Register
          serialPost(ser, "80010008".decode("hex"))
          #if data[l-1] == chr(0x4f):
          # serialPost(ser, "4a".decode("hex"))
        elif s == 10:
          # -> 80 01 00 08
          serialPost(ser, "00000001".decode("hex"))
          #s = 20;
          #if data[l-1] == chr(0xAB):
          # # 0x00 -> Speed = 115200
          # # 0x01 -> Speed = 230400
          # # 0x02 -> Speed = 460800
          # # 0x03 -> Speed = 921600
          # serialPost(ser, "00".decode("hex"))
          # # close comms, bootup completed
          # ser.flushInput()   # flush input buffer, discarding all its contents
          # ser.flushOutput()  # flush output buffer, aborting current output
          # ser.close()
          # # reopen comms at the new speed
          # time.sleep(0.1)
          # ser.port      = "COM3"
          # ser.baudrate      = 115200
          # ser.parity    = serial.PARITY_NONE   # set parity check: no parity
          # ser.open()
          # ser.flushInput()   # flush input buffer, discarding all its contents
          # ser.flushOutput()  # flush output buffer, aborting current output
          # serialPost(ser, "d9".decode("hex"))
        elif s == 11:
          if l == 6: s += 1
        elif s == 12:
          # -> 00 00 00 01
          # -> XX XX        - we hawe a MediaTek MT6253
          serialPost(ser, "A2".decode("hex"))
        elif s == 13:
          # -> A2
          # 80 01 00 04  - Software Version Register
          serialPost(ser, "80010004".decode("hex"))
        elif s == 14:
          # -> 80 01 00 04
          serialPost(ser, "00000001".decode("hex"))
        elif s == 15:
          if l == 6: s += 1
        elif s == 16:
          # -> 00 00 00 01
          # -> XX XX        - 
          # A1  - write to register
          serialPost(ser, "A1".decode("hex"))
        elif s == 17:
          # -> A1        - write command ack
          # 80 03 00 00  - Reset Generation Unit (RGU): Watchdog Timer Control Register
          serialPost(ser, "80030000".decode("hex"))
        elif s == 18:
          # -> 80 03 00 00
          serialPost(ser, "00000001".decode("hex"))
        elif s == 19:
          # -> 00 00 00 01
          # 22 00           - set
          serialPost(ser, "2200".decode("hex"))
        elif s == 20:
          s -= 1
        elif s == 111:
          data   = "d4".decode("hex")
          data0  = chr((ldr2_l >> 24) & int(0xFF))
          data0 += chr((ldr2_l >> 16) & int(0xFF))
          data0 += chr((ldr2_l >>  8) & int(0xFF))
          data0 += chr((ldr2_l      ) & int(0xFF))
          data  += data0
          serialPost(ser, data)
        elif s == 112:
          # zapominaem CRC
          crc = data
          my_crc = summ(data0, 4)
          print "crc    is: " + binascii.b2a_hex(crc)
          print "my_crc is: " + binascii.b2a_hex(my_crc)
          if crc == my_crc:
            send_len = 0
            for i in range((ldr2_l - 1) >> 11):
              send_len = ldr2_l - (i << 11)
              if send_len > 2048: send_len = 2048
              # calculate sum
              ss = i << 11
              su = summ(loader2[ss:ss+send_len], send_len)
              # send command
              data = swapSerialData("f7".decode("hex"))
              data = swapSerialData(loader2[ss:ss+send_len])
              #print "2 crc    is: " + binascii.b2a_hex(data)
              #print "2 my_crc is: " + binascii.b2a_hex(su)
              #print "i: " + str(i)
              sys.stdout.write("\ri: " + str(i))
            sys.stdout.write("\n")
            serialPost(ser, "FF".decode("hex"))
        elif s == 113:
          serialPost(ser, "D010000000".decode("hex"))
        elif s == 114:
          serialPost(ser, "D1".decode("hex"))
        elif s == 115:
          nand_id = (ord(data[8])<<8) + ord(data[9])
          # nado proverit, chto 2,3,4 baity ravny sootvetstvenno 0xEC 0x22 0xFC
          #
          # additionally identify NAND for Swift
          print "Flash...  "
          if   nand_id == int(0x04): print " 16MB (128Mbit) NAND"
          elif nand_id == int(0x14): print " 32MB (256Mbit) NAND"
          elif nand_id == int(0x24): print " 64MB (512Mbit) NAND"
          elif nand_id == int(0x34): print "128MB (  1Gbit) NAND"
          elif nand_id == int(0x0C): print " 16MB (128Mbit) NAND"
          elif nand_id == int(0x1C): print " 32MB (256Mbit) NAND"
          elif nand_id == int(0x2C): print " 64MB (512Mbit) NAND"
          elif nand_id == int(0x3C): print "128MB (  1Gbit) NAND"
          else:              print "Unknown NAND: " + str("%02x" % nand_id)
          # here, the bootup is completed
          # delay slightly (required!)
          time.sleep(0.25)
        else:
          #data = chr(0x44)
          data = chr(0x00)
          print "-> " + binascii.b2a_hex(data)
          #ser.write(data)
    
    data = ser.read()
    print "serial RX: " + binascii.b2a_hex(data)
    
    data = chr(0x44)
    print "-> " + binascii.b2a_hex(data)
    ser.write(data)
    #ser.flush()
    
    data = ser.read()
    print "serial RX: " + binascii.b2a_hex(data)
    
    data = chr(0x51)
    print "-> " + binascii.b2a_hex(data)
    ser.write(data)
    
    data = ser.read()
    print "serial RX: " + binascii.b2a_hex(data)
    
    #print ser.portstr
    time.sleep(0.5)    # give the serial port sometime to receive the data
    numOfLines = 0
    while True:
        response = ser.readline()
        print("read data: " + response)
        numOfLines = numOfLines + 1
        if (numOfLines >= 5):
          break
    ser.close()

   except Exception, e1:
    print "error communicating...: " + str(e1)
    ser.close()
    import traceback
    traceback.print_exc()

   except KeyboardInterrupt:
    print "\nmanual interrupted!"
    ser.close()

  else:
    print "cannot open serial port "

  exit()

#===========================================================

from hktool.hotplug  import windevnotif
#from hktool.bootload import mediatek
from hktool.bootload.mediatek import MTKBootload

from threading import Thread
from time import sleep as Sleep

#----- MAIN CODE -------------------------------------------
if __name__=='__main__':
  Thread(target = windevnotif.run_notify).start()
  Sleep(1)
  port = windevnotif.get_notify()
  print "port_name is: " + port
  #conn_port(port)
  #mediatek.init(port)
  m = MTKBootload(port)
