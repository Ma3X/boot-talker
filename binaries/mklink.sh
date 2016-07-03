#!/bin/bash

easy_install pip
pip install pyudev
pip install pyusb
pip install pyserial
apt-get install statserial
apt-get install setserial

ln -sf ../code/talk.py talk.py
ln -sf ../codes/golang/mtk_loader.go mtk_loader.go