#!/bin/bash

easy_install pip
pip install pyudev
pip install pyusb
pip install pyserial
apt-get install statserial
apt-get install setserial

ln -sf ../code/talk.py talk.py
ln -sf ../codes/golang/mtk_loader.go mtk_loader.go

ln -sf ../codes/python/mtk_lga290_2.py mtk_lga290_2.py
ln -sf ../codes/python/mtk_lga290.py mtk_lga290.py
ln -sf ../codes/python/mtk_texet_tm-510r.py mtk_texet_tm-510r.py
ln -sf ../codes/python/talk.py talk.py
