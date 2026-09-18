from intTypes import *

def nibble(value):
    return UInt(4, value)
def byte(value):
    return UInt(8, value)
def word(value):
    return UInt(16, value)

class CPU:
    def __init__(self, cycles=2):
        self.mem = []
        for i in range(0, 2**16):
            self.mem.append(0)

        #registers
        self.REG = {"A": byte(0x00), "X": byte(0x00), "Y": byte(0x00)}

        #pointers/ counters
        self.PC = word(0x0000) #program counter
        self.SP = word(0x0000) #stack pointer
        self.cycles = cycles

        #flags
        #C #Carry
        #Z #Zero
        #I #Interupt Disable
        #D #Decimal Mode
        #B #Break
        #U #Unused / Always 1
        #V #Overflow
        #N #Negative

        self.SR = {'c': 1, 'z': 1, 'i': 1, 'd': 1, 'b': 1, 'u': 1, 'v': 1, 'n': 1} # Status Register/ Flags

    def check_page(self):
        pass

    def Mem_init(self):
        for i in range(len(self.mem)):
            self.mem[i] = byte(0x00)

    def Reset(self):
        self.PC = word(0xFFFC)
        self.SP = word(0x01FF)

        for i in self.REG.keys():
            self.REG[i] = byte(0x00)

        for i in self.SR.keys():
            self.SR[i] = int(i == "u")

        self.Mem_init()

    def Mem_WriteWord(self, value, address):
        value = word(value)
        self.mem[address] = byte(value & 0xFF)
        self.mem[address + 1] = byte(value >> 8)

        self.cycles -= 2

    def FetchByte(self):
        data = self.mem[self.PC]
        self.PC += 1
        self.cycles -= 1
        return byte(data)

    def FetchWord(self):
        data = word(self.mem[self.PC])
        self.PC += 1

        data |= word(self.mem[self.PC]) << 8
        self.PC += 1
        self.cycles -= 2
        return word(data)

    def FetchWordFromStack(self, adjust):
        data = word(self.mem[self.SP])
        self.SP += 1

        data |= word(self.mem[self.SP]) << 8
        self.check_sp(-1 + adjust)
        self.cycles -= 2
        return word(data)

    def ReadByte(self, address):
        data = self.mem[address]
        self.cycles -= 1
        return byte(data)

    def check_sp(self, adjust: int):
        self.SP += adjust
        self.SP.value = (self.SP.value % 0x0100) + 0x0100

    def LDR(self, register : str, mode):
        register = register.upper()
        match mode:
            case "IM":
                self.REG[register] = self.FetchByte()
            case "ZP":
                ZPADDR = self.FetchByte()
                self.REG[register] = self.ReadByte(ZPADDR)
            case "ZPX":
                if register != "X":
                    ZPAddr = self.FetchByte()
                    ZPAddr += self.REG["X"]
                    self.cycles -= 1
                    self.REG[register] = self.ReadByte(ZPAddr)
            case "ZPY":
                if register == "X":
                    ZPAddr = self.FetchByte()
                    ZPAddr += self.REG["Y"]
                    self.cycles -= 1
                    self.REG["X"] = self.ReadByte(ZPAddr)
            case "ABS":
                addr = self.FetchWord()
                self.cycles -= 1
                self.REG[register] = self.ReadByte(addr)

        self.SR['z'] = self.REG[register] == 0
        self.SR['n'] = self.REG[register] & 0b10000000 > 0

    def JSR(self):
        SubAddr = self.FetchWord()
        self.check_sp(2)
        self.Mem_WriteWord(self.PC, word(self.SP))
        self.PC = SubAddr
        self.cycles -= 2

    def RTS(self):
        RetAddr = self.FetchWordFromStack(-2)
        self.PC = RetAddr + 1
        self.cycles -= 4


    def JMP(self, mode):
        match mode:
            case "ABS":
                JmpAddr = self.FetchWord()
                self.PC = JmpAddr
                self.cycles -= 1

    def NOP(self):
        self.cycles -= 2

    def AND(self, mode):
        match mode:
            case "IM":
                self.REG["A"] &= self.FetchByte()
                self.cycles -= 1

        self.SR['z'] = self.REG['A'] == 0
        self.SR['n'] = self.REG['A'] & 0b10000000 > 0

    def __TRN(self, start, end):
        if start != end:
            if (start == "SP" and end == "X") or (start == "X" and end == "SP"):
                match start:
                    case _:
                        pass
            if (start != "X" and end != "Y") or (start != "Y" and end != "X"):
                self.REG[end] = self.REG[start]
                self.cycles -= 2

        self.SR['z'] = self.REG[end] == 0
        self.SR['n'] = self.REG[end] & 0b10000000 > 0

    def INCR(self, register: str):
        self.REG[register] += 1

        self.SR['z'] = self.REG[register] == 0
        self.SR['n'] = self.REG[register] & 0b10000000 > 0

    def DECR(self, register: str):
        self.REG[register] -= 1

        self.SR['z'] = self.REG[register] == 0
        self.SR['n'] = self.REG[register] & 0b10000000 > 0

    def execute(self):
        while self.cycles > 0:
            ins = int(self.FetchByte())
            match ins:

                #LDA
                case 0xA9:
                    self.LDR("A", "IM")
                case 0xA5:
                    self.LDR("A", "ZP")
                case 0xB5:
                    self.LDR("A", "ZPX")
                case 0xAD:
                    self.LDR("A", "ABS")
                #LDX
                case 0xA2:
                    self.LDR("X", "IM")
                case 0xA6:
                    self.LDR("X", "ZP")
                case 0xB6:
                    self.LDR("X", "ZPY")
                case 0xAE:
                    self.LDR("X", "ABS")
                #LDY
                case 0xA0:
                    self.LDR("Y", "IM")
                case 0xA4:
                    self.LDR("Y", "ZP")
                case 0xB4:
                    self.LDR("Y", "ZPX")
                case 0xAC:
                    self.LDR("Y", "ABS")

                #Transfer
                case 0xAA:
                    self.__TRN("A", "X")
                case 0x8A:
                    self.__TRN("X", "A")
                case 0xA8:
                    self.__TRN("A", "Y")
                case 0x98:
                    self.__TRN("Y", "A")

                case 0x20: #JSR
                    self.JSR()
                case 0x60: #RTS
                    self.RTS()

                case 0x4C:
                    self.JMP("ABS")

                case 0x29:
                    self.AND("IM")

                case 0xEA: #NOP
                    self.NOP()

                #INC/DEC
                case 0xE8:
                    self.INCR("X")
                case 0xC8:
                    self.INCR("Y")
                case 0xCA:
                    self.DECR("X")
                case 0x88:
                    self.DECR("Y")

    def __repr__(self):
        char_display = ''
        byte_display = []
        res = '[0;38;5;201mADDR: [0m' + ' '.join(
            f'X[38;5;93m{i:X}[0m' for i in range(16)) + ' |[38;5;198m ASCII CHARACTERS\n[0m' + f'{"_" * 72}\n'
        for i in range(0, 65536, 16):
            for j in range(i, i + 16):
                current_byte = self.mem[j].value
                if 32 < current_byte < 127:
                    char_display += chr(current_byte)
                else:
                    char_display += '.'
                byte_display += [f'{current_byte:02X}']
            res += f'[38;5;201m{i:04X}:[38;5;93m {" ".join(byte_display)} [0;28m|[38;5;198m {char_display}\n'
            char_display = ''
            byte_display = []
        return res + f'[0mFLAGS: czidbuvn REGISTERS: A: 0x{self.REG["A"].value:02X} X: 0x{self.REG["X"].value:02X} Y: 0x{self.REG["Y"].value:02X}\n       {"".join(str(int(i)) for i in self.SR.values())} POINTERS: PC: 0x{self.PC.value:04X} SP: 0x{self.SP.value:04X} CYCLES LEFT: {self.cycles}\n'

# cpu = CPU(204)
# cpu.Reset()
#
# cpu.mem[0xFFFC] = byte(0x4C)
# cpu.Mem_WriteWord(0x4240, 0xFFFD)
# cpu.Mem_WriteWord(0x84A9, 0x4240)
#
# cpu.execute()
# print(cpu)
