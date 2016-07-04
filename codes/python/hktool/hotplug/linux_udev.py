#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyudev
from time import strftime
from pprint import pprint

import threading
from time import sleep as Sleep

#--------------------------------------------------------------------

class Notification(threading.Thread):
  event     = threading.Event()
  port_name = None
  hwnd      = None
  
  observer  = None
  current_devices={}

  def timestamp():
    return strftime('%Y/%m/%d %H:%M:%S')

  def decode_device_info(device):
    ''' Accept a device. Return a dict of attributes of given device. 
        Clean up all strings in the process and make pretty.
    '''
    if 'ID_VENDOR' in device:
        vendor = device['ID_VENDOR'].replace('_',' ')
    else:
        vendor = ''
    if 'ID_MODEL' in device:
        model = device['ID_MODEL'].replace('_',' ')
    else:
        model = ''
    #vendor = "0[ID_VENDOR]".format(device).replace('_',' ')
    #model = "0[ID_MODEL]".format(device).replace('_',' ')
    try:
        serial = device['ID_SERIAL_SHORT']
        #serial = "0[ID_SERIAL_SHORT]".format(device)
    except:
      if 'ID_SERIAL' in device:
        serial = device['ID_SERIAL']
      else:
        serial = ''
        #serial = "0[ID_SERIAL]".format(device)
    return({'vendor':vendor, 'model':model, 'serial':serial})

  def log_device_event(device):
    '''Add or remove device to/from the dict of currently plugged in devices. Return the dict.
    '''
    global current_devices
    #print device
    if 'DEVNAME' in device:
        devname = device['DEVNAME']
    else:
        devname = ''
    #devname = "0[DEVNAME]".format(device)
    if device.action == 'add':
        current_devices[devname] = (decode_device_info(device), timestamp())
    if device.action == 'remove':
      try:
        del current_devices[devname]
      except KeyError:
        print '\n'
    return(current_devices)

  def formatted_listing(device_dict):
    ''' Print a nicely formatted listing of devices currently in the device_dict 
    '''
    print('\n' + '-'*15 + ' Currently Plugged In: ' + '-'*15)
    for device_record in device_dict.keys():
        print("{0[vendor]} {0[model]}: {0[serial]}".format(device_dict[device_record][0]))

  def print_device_event(self, device):
    '''Print details of a device added or removed
    '''
    #print('background event {0.action}: {0.device_type}'.format(device))
    #print(dir(device))
    print(list(device.items()))
    #print("device.action: device add")
    if device.action == 'add':
        #print(timestamp()+" | Device {0[ID_VENDOR]} {0[ID_MODEL]} with serial number {0[ID_SERIAL]} was plugged in. ----- {0[DEVNAME]}".format(device))
        #print(timestamp()+" | Device-> ID_VENDOR: {0[ID_VENDOR]}".format(device))
        #print(timestamp()+" |           ID_MODEL: {0[ID_MODEL]} with serial number:".format(device))
        #print(timestamp()+" |          ID_SERIAL: {0[ID_SERIAL]} was plugged in:".format(device))
        #print(timestamp()+" |            DEVNAME: {0[DEVNAME]}".format(device))
        print("device added")
    elif device.action == 'remove':
        #print(timestamp()+" | Device {0[vendor]} {0[model]} with serial number {0[serial]} was removed".format(self.current_devices[device[devname][1]]))
        print("device removed")
    else:
        print("act: " + str(device.action));
    if device.subsystem == 'tty':
        print 'tty: ' + device['DEVNAME']

    if not 'ttyACM' in device['DEVNAME']:
        #ser_port = device['DEVNAME']
        self.port_name = device['DEVNAME']
        self.event.set()

        #Sleep(1)
        #? self.observer.stop()
        self.observer.send_stop()
        #Sleep(1)

  def process_device_event(self, device):
    self.current_devices
    #pprint(device, indent=2)
    #log_device_event(device)
    self.print_device_event(device)
    #formatted_listing(current_devices)

  def __init__(self, isBreakable=True):
    self.event.clear()

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    #monitor.filter_by('block')
    monitor.filter_by('tty') # without filters view all messages
    self.observer = pyudev.MonitorObserver(monitor, callback=self.process_device_event, name='monitor-observer')
    self.observer.daemon = False
    self.observer.start()

  def re__init__(self, isBreakable=True):
    self.event.clear()

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    #monitor.filter_by('block')
    monitor.filter_by('tty')
    monitor.start()
    for device in iter(monitor.poll, None):
        #print(list(device.items()))
        #if device.subsystem == 'tty' and device.action == 'add' and device['ID_MODEL'] == 'MT6235':
        #if device.subsystem == 'tty' and device.action == 'add' and device['ID_USB_DRIVER'] == 'qcaux':
        if device.subsystem == 'tty' and device.action == 'add' and device['ID_USB_DRIVER'] == 'qcaux':
	    print(list(device.items()))
	    print 'tty: ' + device['DEVNAME']
	    self.port_name = device['DEVNAME']
	    if isBreakable: break

    self.event.set()
    Sleep(2)
    pass

  def onWait(self):
    self.event.wait()
    return self.port_name

  def kill(self):
    del self

  def __del__(self):
    print "del obj"
    #self.close()

  #
  # WM_DEVICECHANGE:
  #  wParam - type of change: arrival, removal etc.
  #  lParam - what's changed?
  #    if it's a volume then...
  #  lParam - what's changed more exactly
  #
  def onDeviceChange (self, hwnd, msg, wparam, lparam):
    # http://blog.carduner.net/2009/03/01/information-hiding-in-python-using-metaclasses/
    # http://stackoverflow.com/questions/70528/why-are-pythons-private-methods-not-actually-private
    try :
      function_call = inspect.stack()[1][4][0].strip()

      # See if the function_call has "self." in the begining
      matched = re.match( '^self\.', function_call )
      if not matched :
          print 'This is Private Function, Go Away'
          return

    except :
      print 'This is Private Function, Go Away'
      return

    # This is the real Function, only accessible inside class #
    print 'Hey, Welcome in to function'
        
    #dev_broadcast_hdr = DEV_BROADCAST_HDR.from_address (lparam)

    #if wparam == DBT_DEVICEARRIVAL:
    #  print "Something's arrived"
    #  #print(list(dev_broadcast_hdr.items()))
    #
    #  if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYPE_PORT:
    #    print "It's a port!"
    #    dev_broadcast_port = DEV_BROADCAST_PORT.from_address (lparam)
    #    print(dev_broadcast_port.dbcp_size)
    #    print(dev_broadcast_port.dbcp_devicetype)
    #    print(dev_broadcast_port.dbcp_reserved)
    #    print(dev_broadcast_port.dbcp_name)
    #    # see: http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html#local-scope
    #    #port_name = dev_broadcast_port.dbcp_name
    #    #print "port_name is: " + port_name
    #    #conn_port(port_name)
    #    self.port_name = dev_broadcast_port.dbcp_name
    #    self.event.set()
    #
    #  if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYP_VOLUME:
    #    print "It's a volume!"
    #
    #    dev_broadcast_volume = DEV_BROADCAST_VOLUME.from_address (lparam)
    #    if dev_broadcast_volume.dbcv_flags & DBTF_MEDIA:
    #      print "with some media"
    #      drive_letter = drive_from_mask (dev_broadcast_volume.dbcv_unitmask)
    #      print "in drive", chr (ord ("A") + drive_letter)
    #
    return 1

#=====================================================================
# Header procedures 

w = None

def run_notify():
  global w
  w = Notification ()
  print "pre PumpMessages"
  #win32gui.PumpMessages ()
  #print "post PumpMessages"

def get_notify():
  global w
  print "pre onWait"
  port = w.onWait()
  w.kill()
  del w
  import gc
  gc.collect()
  return port

