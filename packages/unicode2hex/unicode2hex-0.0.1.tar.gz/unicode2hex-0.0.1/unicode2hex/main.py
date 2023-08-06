# -*- coding: utf-8 -*-
import sys
import re
# get utf-8 code points to hex codes
# i.e. \u2318 to \xe2\x8c\x98

def main(argv):
    hex_arrays=[]
    pattern = re.compile(r"\\?[Uu]?(?P<value>[0-9A-Fa-f]{1,6})")
    for val in argv:
        res=pattern.match(val)
        if res and len(res.group("value")):
            hex_val=int(res.group("value"),16)
            hex_str="{:x}".format(hex_val)
            unicode_val=hex(hex_val)
            hex_arrays.append([unicode_val,codepoint_to_hex(hex_str)])
        elif len(val)==1:
            unicode_val=hex(ord(val))
            hex_str="{:x}".format(int(unicode_val,16))
            hex_arrays.append([unicode_val,codepoint_to_hex(hex_str)])

    for row in hex_arrays:
        val,line = row[0],row[1]
        hex_bytes=r"\x".join(line)
        hex_bytes=r"\x"+hex_bytes
        print(bytes.fromhex("".join(line)).decode("utf-8")," <-> ",hex_bytes," <-> ",val)

'''
# utf8 specification

0x00  - 0x7f
1 byte utf8:
    0ZZZ ZZZZ

0x80 - 0x07ff
2 byte utf8:
    110Y YYYY
    10ZZ ZZZZ

0x0800 - 0xffff
3 byte utf8:
    1110 XXXX
    10YY YYYY
    10ZZ ZZZZ

0x10000 - 0x10ffff
4 byte utf8:
    1111 0VVV
    10WW XXXX
    10YY YYYY
    10ZZ ZZZZ
'''


def codepoint_to_hex(codepoint):
    hex_bytes=chr(int(codepoint,16)).encode('utf-8')
    # print(repr(chr(int(codepoint,16))),end=" ")
    hex_str=hex_bytes.hex()
    arr=[]
    for i in range(0,len(hex_str),2):
        arr.append(hex_str[i:i+2])
    return arr

def run():
    main(sys.argv[1:])

if __name__ == '__main__':
    run()
