"""Microcode for my 8-bit computer"""

import sys


def bit(n):
    return 1 << n


# control lines
HLT = bit(15)                   # Halt
MI = bit(14)                    # Memory (address) in
RI = bit(13)                    # RAM (value) in
RO = bit(12)                    # RAM (value) out
IO = bit(11)                    # Instruction register out
II = bit(10)                    # Instruction register in
AI = bit(9)                     # A register in
AO = bit(8)                     # A register out
EO = bit(7)                     # Sum register out
SU = bit(6)                     # Subtract
BI = bit(5)                     # B register in
OI = bit(4)                     # Output register in
CE = bit(3)                     # Program counter enable
CO = bit(2)                     # Program counter out
JM = bit(1)                     # Jump (program counter in)
FI = bit(0)                     # Flag register in

# each instruction starts with these two micro-instructions
find_instruction = CO | MI
load_instruction = RO | II | CE

# each instruction has six remaining micro-instructions
basic_microcode = [
    [0,       0,       0,                 0, 0, 0],  # 0000 - NOP
    [IO | MI, RO | AI, 0,                 0, 0, 0],  # 0001 - LDA
    [IO | MI, RO | BI, EO | AI | FI,      0, 0, 0],  # 0010 - ADD
    [IO | MI, RO | BI, EO | AI | SU | FI, 0, 0, 0],  # 0011 - SUB
    [IO | MI, AO | RI, 0,                 0, 0, 0],  # 0100 - STA
    [IO | AI, 0,       0,                 0, 0, 0],  # 0101 - LDI
    [IO | JM, 0,       0,                 0, 0, 0],  # 0110 - JMP
    [0,       0,       0,                 0, 0, 0],  # 0111 - JC
    [0,       0,       0,                 0, 0, 0],  # 1000 - JZ
    [0,       0,       0,                 0, 0, 0],  # 1001
    [0,       0,       0,                 0, 0, 0],  # 1010
    [0,       0,       0,                 0, 0, 0],  # 1011
    [0,       0,       0,                 0, 0, 0],  # 1100
    [0,       0,       0,                 0, 0, 0],  # 1101
    [AO | OI, 0,       0,                 0, 0, 0],  # 1110 - OUT
    [HLT,     0,       0,                 0, 0, 0]   # 1111 - HLT
]

# the flags change the behaviour of conditional instructions
# there are four branches
FLAGS_Z0C0 = 0
FLAGS_Z0C1 = 1
FLAGS_Z1C0 = 2
FLAGS_Z1C1 = 3

# conditional instructions
JC = 0b0111
JZ = 0b1000

branches = 4
instructions = 16
steps = 8
microcode_int = [
    [
        [find_instruction, load_instruction] + instruction
        for instruction in basic_microcode
    ]
    for _ in range(branches)
]
microcode_int[FLAGS_Z0C1][JC][2] = IO | JM
microcode_int[FLAGS_Z1C0][JZ][2] = IO | JM
microcode_int[FLAGS_Z1C1][JC][2] = IO | JM
microcode_int[FLAGS_Z1C1][JZ][2] = IO | JM

# address structure:
# pin  meaning
# 10   not used (zero)
#  9   zero flag
#  8   carry flag
#  7   chip select
#  6   opcode
#  5   opcode
#  4   opcode
#  3   opcode
#  2   step
#  1   step
#  0   step

microcode = bytearray(1024)
for addr in range(1024):
    flags = (addr >> 8) & 0x3
    chip_select = (addr >> 7) & 0x1
    opcode = (addr >> 3) & 0xf
    step = addr & 0x7

    if chip_select == 1:
        microcode[addr] = (microcode_int[flags][opcode][step] >> 8) & 0xff
    else:
        microcode[addr] = microcode_int[flags][opcode][step] & 0xff

sys.stdout.buffer.write(microcode)
