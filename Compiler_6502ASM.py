from intTypes import *
from Main_6502 import *

cpu = CPU()

lines = []

def READFile(file_name: str):
    temp_str = ''
    with open(file_name, "r") as file:
        temp_str = file.read()

    out_str = ''
    # split into lines of code
    for char in temp_str:
        if char != "\n":
            out_str += char
        elif char == "\n":
            if out_str != '':
                lines.append(out_str)
                out_str = ''
    # adds last line of code to list
    if out_str != '':
        lines.append(out_str)
        out_str = ''

def FreeWriteWord(value, address):
    value = word(value)
    cpu.mem[address] = byte(value & 0xFF)
    cpu.mem[address + 1] = byte(value >> 8)

data = {}
def compile():
    #seperate lines into opcodes
    for line in lines:
        temp = ''
        line_num = ''
        ops = []
        for char in line:
            if char != " ":
                temp += char
            else:
                ops.append(temp)
                temp = ""
        ops.append(temp)

        data[ops.pop(0)] = ops

    if "SETCYCLES" in data.keys():
        cpu.cycles = int(data["SETCYCLES"][0])
    cpu.Reset()

    del data["SETCYCLES"]

    for key in data.keys():
        if data[key][0] == 'JMP':
            if "(" in data[key][1]:
                cpu.mem[int(key, 16)] = byte(0x6C)
            else:
                cpu.mem[int(key, 16)] = byte(0x4C)

        if data[key][0] == 'JSR':
            cpu.mem[int(key, 16)] = byte(0x20)

        if data[key][0] == 'LDA':
            if "#$" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0xA9)
            elif "$" in data[key][-1] and ",X" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0xB5)
            elif "$" in data[key][-1] and len(data[key][-1]) < 5:
                cpu.mem[int(key, 16)] = byte(0xA5)
            elif len(data[key][1]) == 5:
                cpu.mem[int(key, 16)] = byte(0xAD)

        if data[key][0] == 'LDX':
            if "#$" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0xA2)
            elif "$" in data[key][-1] and ",Y" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0xB6)
            elif "$" in data[key][-1] and len(data[key][-1]) < 5:
                cpu.mem[int(key, 16)] = byte(0xA6)
            elif len(data[key][1]) == 5:
                cpu.mem[int(key, 16)] = byte(0xAE)

        if data[key][0] == 'LDY':
            if "#$" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0xA0)
            elif "$" in data[key][-1] and ",X" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0xB4)
            elif "$" in data[key][-1] and len(data[key][-1]) < 5:
                cpu.mem[int(key, 16)] = byte(0xA4)
            elif len(data[key][1]) == 5:
                cpu.mem[int(key, 16)] = byte(0xAC)

        if data[key][0] == 'TAX':
            cpu.mem[int(key, 16)] = byte(0xAA)
        if data[key][0] == 'TXA':
            cpu.mem[int(key, 16)] = byte(0x8A)
        if data[key][0] == 'TAY':
            cpu.mem[int(key, 16)] = byte(0xA8)
        if data[key][0] == 'TYA':
            cpu.mem[int(key, 16)] = byte(0x98)

        if data[key][0] == 'INX':
            cpu.mem[int(key, 16)] = byte(0xE8)
        if data[key][0] == 'DEX':
            cpu.mem[int(key, 16)] = byte(0xCA)
        if data[key][0] == 'INY':
            cpu.mem[int(key, 16)] = byte(0xC8)
        if data[key][0] == 'DEY':
            cpu.mem[int(key, 16)] = byte(0x88)

        if data[key][0] == 'NOP':
            cpu.mem[int(key, 16)] = byte(0xEA)

        if data[key][0] == 'AND':
            if "#$" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0x29)
            elif "$" in data[key][-1] and ",X" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0x35)
            elif "$" in data[key][-1]:
                cpu.mem[int(key, 16)] = byte(0x25)

        out = ''
        for char in data[key][-1]:
            if char in "0123456789ABCDEF":
                out += char

        if len(out) == 4:
            out = word(int(out, 16))
            FreeWriteWord(out, word(int(key, 16)) + 1)
        elif len(out) == 2:
            out = word(int(out, 16))
            cpu.mem[word(int(key, 16)) + 1] = out


READFile('main.asm6502')
compile()
cpu.execute()
print(cpu)