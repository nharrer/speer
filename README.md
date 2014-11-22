speer
=====

<b>S</b>amsung <b>P</b>rinter <b>EE</b>prom <b>R</b>esetter for Raspberry Pi

Speer is a python script that can backup, restore and reset the content of the EEPROM of toner cartridges for the Samsung CLP-510 series printers.

The script is intended to be used with a Rasperry Pi connected to a toner catridge. 

The toner catridges for the CLP-510 contain a ST24C04 which is a 4 Kbit Serial I2C Bus EEPROM. It can be contected with three wires to the I2C-Bus on the GPIO header of a Raspberry Pi. This script then reads from and writes to the EEPROM.

In theory, it should run on any other Platform which provides the smbus python package. It was however only tested with a Rasperry Pi.


Wiring Plan
-----------


    Toner cartridge:
    
    +--------------------------------------------------------+
    |       / \                                 .            |
    |       \ /               +---------------+            O +
    |                         | [D]  [G]  [C] |             /
    +------------------------------------------------------+
    
           D = Data    <connect-to>  Raspberry Pi pin 3
           G = Ground  <connect-to>  Raspberry Pi pin 6
           C = Clock   <connect-to>  Raspberry Pi pin 5


Usage
-----
    
    usage: speer.py [-b <filename>] [-x] [-r <filename>] [-z] [-w] [-h]
                    [--bus <bus>] [--addr <addr>]
    
    commands:
      -b <filename>  backup EEPROM to file
      -x             output hex dump of EEPROM
      -r <filename>  restore EEPROM from file
      -z             auto-zero page counter in EEPROM
      -w             print wiring information
    
    optional arguments:
      -h, --help     show this help message and exit
      --bus <bus>    i2c-bus (default: 1)
      --addr <addr>  i2c-address (default: 0x56)


