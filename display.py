"""A 7-segment display has 8 LEDs (including the decimal point, which we don't use)
They are labelled:

    a
   ---
 f|   |b
   -g-
 e|   |c
   ---  .
    d   p

The data pins on the EEPROM are wired up such that the bits in each byte correspond to
segments like:

bit     76543210
segment pabcdefg
"""

import sys

# these encode the basic 16 hex digits for a single 7-segment display
# for common anode the bits are off, for common cathode they are on
COMMON_ANODE = (
    b"\x81\xcf\x92\x86\xcc\xa4\xa0\x8f\x80\x84\x88\xe0\xb1\xc2\xb0\xb8"
)
COMMON_CATHODE = (
    b"\x7e\x30\x6d\x79\x33\x5b\x5f\x70\x7f\x7b\x77\x1f\x4e\x3d\x4f\x47"
)

output = bytearray(2048)
data = COMMON_CATHODE

# unsigned output
for addr in range(256):
    # units
    output[addr] = data[addr % 10]
    # tens
    output[addr + 0x100] = data[(addr//10) % 10]
    # hundreds
    output[addr + 0x200] = data[(addr//100)]
    # thousands
    output[addr + 0x300] = 0


def s2u(i):
    """Signed to unsigned (8-bit)"""
    if i < 0:
        return i+256
    else:
        return i


# signed output
for addr in range(-128, 128):
    # units
    output[s2u(addr) + 0x400] = data[abs(addr) % 10]
    # tens
    output[s2u(addr) + 0x500] = data[abs(addr//10) % 10]
    # hundreds
    output[s2u(addr) + 0x600] = data[abs(addr//100)]
    # thousands
    output[s2u(addr) + 0x700] = 1 if addr < 0 else 0

sys.stdout.buffer.write(output)
