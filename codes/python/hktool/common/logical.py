#!/usr/bin/env python
# -*- coding: utf-8 -*-

def _logical_xor(str1, str2):
    return bool(str1) ^ bool(str2)

# http://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
#You can convert the characters to integers and xor those instead:
# l = [ord(a) ^ ord(b) for a,b in zip(s1,s2)]
def sxor(s1, s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
    
def words_xor(data):
    #tt = int("0000", 16)
    #tt = 0x0000
    #tt = "\x00\x00"
    tt = "0000".decode('hex')
    for i in range(0, len(data), 2):
        ss = data[i:i+2]
        tt = sxor(tt, ss)
    return tt

def _words_xor(data):
    #tt = int("0000", 16)
    tt = "0000".decode('hex')
    print "type(tt): " + str(type(tt))
    for i in range(0, len(data), 2):
        ss = data[i:i+2]
        print "type(ss): " + str(type(ss))
        zz = bytes(data[i:i+2])
        print "type(zz): " + str(type(zz))
        #tt = tt ^ int(data[i:i+2])
        tt = tt ^ zz
        print "type(tt): " + str(type(tt))
    return tt.tostring()

def word_byteswap(data):
    import array
    a = array.array('H', data)
    a.byteswap()
    return a.tostring()

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

    # [input[i:i+n] for i in range(0, len(input), n)]        # use xrange in py2k