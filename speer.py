#!/usr/bin/python -u

# speer - Samsung Printer EEprom Reset

from __future__ import print_function

import sys
import os
import time
import argparse
import binascii
import string

try:
    import smbus
except ImportError:
    print('Module smbus not found! It probably needs to be installed with:', file=sys.stderr)
    print('', file=sys.stderr)
    print('apt-get install python-smbus', file=sys.stderr)
    os._exit(1)

# default values
I2C_BUS = 1
I2C_ADDR = 0x56
LEN = 0x100


def read_eeprom():
    bus = smbus.SMBus(I2C_BUS)

    buf = bytearray(LEN)
    for addr in range(0, LEN):
        bus.write_byte(I2C_ADDR, addr)
        x = bus.read_byte(I2C_ADDR)
        buf[addr] = x
    return buf

def write_eeprom(buf):
    bus = smbus.SMBus(I2C_BUS)

    addr = 0
    print('Writing {0} bytes:'.format(len(buf)))
    for b in buf:
        sys.stdout.write('.')
        bus.write_byte_data(I2C_ADDR, addr, b)
        addr = addr + 1
        # wait 5ms or else we would get an error message
        time.sleep(0.001 * 5)
    print('ok')

def readfile(filename):
    buf = bytearray()
    with open(filename, "rb") as f:
        b = f.read(1)
        while b != b"":
            buf.append(b)
            b = f.read(1)
    return buf

def writefile(filename, buf):
    with open(filename, "wb") as f:
        b = f.write(buf)

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def hexline(addr, block):
    hex = binascii.hexlify(block)
    hex = hex + (16 - len(block)) * '  '
    hex = ' '.join(hex[i:i+2] for i in xrange(0,len(hex),2))
    hex = ' '.join(hex[i:i+(3*8)] for i in xrange(0,len(hex),(3*8)))
    p = ''.join((chr(x) if chr(x) in string.printable else '.') for x in block)
    hex = ('%08x  ' % addr) + hex + '  |' + p + '|'
    return hex

def hexdump(buf):
    addr = 0
    blen = 16
    for block in chunks(buf, blen):
        print(hexline(addr, block))
        addr = addr + blen

def print_wiring():
    print()
    print('Toner cartridge:')
    print()
    print('+--------------------------------------------------------+')
    print('|       / \                                 .            |')
    print('|       \ /               +---------------+            O +')
    print('|                         | [D]  [G]  [C] |             /')
    print('+------------------------------------------------------+')
    print('')
    print('       D = Data    <connect-to>  raspberry pin 3')
    print('       G = Ground  <connect-to>  raspberry pin 6')
    print('       C = Clock   <connect-to>  raspberry pin 5')
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)

    group = parser.add_argument_group('commands')
    group.add_argument('-b', dest='backup', metavar="<filename>", help="backup EEPROM to file")
    group.add_argument('-x', dest='hexdump', action='store_true', help="output hex dump of EEPROM")
    group.add_argument('-r', dest='restore', metavar="<filename>", help="restore EEPROM from file")
    group.add_argument('-z', dest='zero', action='store_true', help="auto-zero page counter in EEPROM")
    group.add_argument('-w', action='store_true', help="print wiring information")

    group2 = parser.add_argument_group('optional arguments')
    group2.add_argument('-h', '--help', action='store_true', help="show this help message and exit")
    group2.add_argument('--bus', type=int, metavar="<bus>", default=I2C_BUS, help="i2c-bus (default: {0})".format(I2C_BUS))
    group2.add_argument('--addr', metavar="<addr>", default=str(I2C_ADDR), help="i2c-address (default: 0x{0:02x})".format(I2C_ADDR))

    args = parser.parse_args()

    cmd = 0
    if args.backup is not None:
        cmd = cmd + 1
    if args.restore is not None:
        cmd = cmd + 1
    if args.zero:
        cmd = cmd + 1
    if cmd > 1:
        parser.error('only one of -b, -r or -z is allowed')

    if cmd == 0:
        if args.hexdump:
            pass
        elif args.w:
            print_wiring()
            os._exit(0)
        else:
            parser.print_help()
            os._exit(0)

    # set optional values    
    I2C_BUS = args.bus
    try:
        I2C_ADDR = int(args.addr, 0)
    except ValueError:
        I2C_ADDR = -1

    if I2C_ADDR < 3 or I2C_ADDR > 0x77:
        parser.error("invalid number '{0}' for i2c-addri (must be between 0x03 and 0x77)".format(args.addr))

    
    if args.restore is not None:
        print('restoring EEPROM from file {0}'.format(args.restore))
        buf = readfile(args.restore)
        write_eeprom(buf)

    if args.zero:
        #print('setting counter to zero')
        parser.error('-z not implemented yet')

    if args.backup is not None or args.hexdump:
        buf = read_eeprom()
        if args.hexdump:
            hexdump(buf)
        if args.backup is not None:
            print('backing up EEPROM to file {0}'.format(args.backup))
            writefile(args.backup, buf)

