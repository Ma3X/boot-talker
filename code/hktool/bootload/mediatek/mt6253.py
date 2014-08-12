#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_bootcode_first():
  return open(os.path.join(__location__, "mt6253.bin"), "rb").read()

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
