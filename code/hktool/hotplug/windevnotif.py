import win32api, win32con, win32gui
import threading
import ctypes
from ctypes import *

#
# Device change events (WM_DEVICECHANGE wParam)
#
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEQUERYREMOVE = 0x8001
DBT_DEVICEQUERYREMOVEFAILED = 0x8002
DBT_DEVICEMOVEPENDING = 0x8003
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVICETYPESSPECIFIC = 0x8005
DBT_CONFIGCHANGED = 0x0018

#
# type of device in DEV_BROADCAST_HDR
#
DBT_DEVTYP_OEM = 0x00000000
DBT_DEVTYP_DEVNODE = 0x00000001
DBT_DEVTYP_VOLUME = 0x00000002
DBT_DEVTYPE_PORT = 0x00000003
DBT_DEVTYPE_NET = 0x00000004

#
# media types in DBT_DEVTYP_VOLUME
#
DBTF_MEDIA = 0x0001
DBTF_NET = 0x0002

TCHAR = c_char * 256
WORD  = c_ushort
DWORD = c_ulong

class DEV_BROADCAST_HDR (Structure):
  _fields_ = [
    ("dbch_size", DWORD),
    ("dbch_devicetype", DWORD),
    ("dbch_reserved", DWORD)
  ]

class DEV_BROADCAST_VOLUME (Structure):
  _fields_ = [
    ("dbcv_size", DWORD),
    ("dbcv_devicetype", DWORD),
    ("dbcv_reserved", DWORD),
    ("dbcv_unitmask", DWORD),
    ("dbcv_flags", WORD)
  ]

class DEV_BROADCAST_PORT (Structure):
  _fields_ = [
    ("dbcp_size", DWORD),
    ("dbcp_devicetype", DWORD),
    ("dbcp_reserved", DWORD),
    ("dbcp_name", TCHAR)
  ]

import signal
import sys
import os
import thread
def sig_handler(signal, frame):
    global s, ser
    print '\nYou pressed Ctrl+C!'
    os._exit(0)
    #sys.exit(0)
    #thread.interrupt_main()

#signal.signal(signal.SIGINT, sig_handler)

def drive_from_mask (mask):
  n_drive = 0
  while 1:
    if (mask & (2 ** n_drive)): return n_drive
    else: n_drive += 1

class Notification(threading.Thread):
  event     = threading.Event()
  port_name = None
  hwnd      = None

  def __init__(self):
    #threading.Thread.__init__(self)
  
    # def run(self):
    message_map = {
      win32con.WM_DEVICECHANGE : self.onDeviceChange
    }

    wc = win32gui.WNDCLASS ()
    hinst = wc.hInstance = win32api.GetModuleHandle (None)
    wc.lpszClassName = "DeviceChangeDemo"
    wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
    wc.hCursor = win32gui.LoadCursor (0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW
    wc.lpfnWndProc = message_map
    classAtom = win32gui.RegisterClass (wc)
    style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
    self.hwnd = win32gui.CreateWindow (
      classAtom,
      "Device Change Demo",
      style,
      0, 0,
      win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
      0, 0,
      hinst, None
    )
    self.event.clear()

  def onWait(self):
    self.event.wait()
    return self.port_name

  def kill(self):
    #win32gui.DestroyWindow(self.hwnd)
    win32gui.SendMessage(self.hwnd, win32con.WM_CLOSE)
    ctypes.windll.user32.PostQuitMessage(0)
    del self

  def __del__(self):
    #win32gui.DestroyWindow(self.hwnd)
    print "del obj"
    #self.close()

  def onDeviceChange (self, hwnd, msg, wparam, lparam):
    #
    # WM_DEVICECHANGE:
    #  wParam - type of change: arrival, removal etc.
    #  lParam - what's changed?
    #    if it's a volume then...
    #  lParam - what's changed more exactly
    #
    dev_broadcast_hdr = DEV_BROADCAST_HDR.from_address (lparam)

    if wparam == DBT_DEVICEARRIVAL:
      print "Something's arrived"
      #print(list(dev_broadcast_hdr.items()))

      if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYPE_PORT:
        print "It's a port!"
        dev_broadcast_port = DEV_BROADCAST_PORT.from_address (lparam)
        print(dev_broadcast_port.dbcp_size)
        print(dev_broadcast_port.dbcp_devicetype)
        print(dev_broadcast_port.dbcp_reserved)
        print(dev_broadcast_port.dbcp_name)
        # see: http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html#local-scope
        #port_name = dev_broadcast_port.dbcp_name
        #print "port_name is: " + port_name
        #conn_port(port_name)
        self.port_name = dev_broadcast_port.dbcp_name
        self.event.set()

      if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYP_VOLUME:
        print "It's a volume!"

        dev_broadcast_volume = DEV_BROADCAST_VOLUME.from_address (lparam)
        if dev_broadcast_volume.dbcv_flags & DBTF_MEDIA:
          print "with some media"
          drive_letter = drive_from_mask (dev_broadcast_volume.dbcv_unitmask)
          print "in drive", chr (ord ("A") + drive_letter)

    return 1

#=====================================================================
# Header procedures 

w = None

def run_notify():
  global w
  w = Notification ()
  print "pre PumpMessages"
  win32gui.PumpMessages ()
  print "post PumpMessages"

def get_notify():
  global w
  print "pre onWait"
  port = w.onWait()
  w.kill()
  del w
  import gc
  gc.collect()
  return port
