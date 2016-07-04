import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_bootcode_first():
  return open(os.path.join(__location__, "loader1.bin"), "rb").read()

def load_bootcode_second():
  return open(os.path.join(__location__, "loader2.bin"), "rb").read()
