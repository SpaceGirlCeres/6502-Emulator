class UInt:
    def __init__(self, bits=8, value=0):
        if 65 > bits > 0:
            self.bits = bits
        elif bits > 64:
            self.bits = 64
        else:
            self.bits = 1

        self.value = self.clamp(value, self.bits)

    # Helper Functions
    def clamp(self, value, bit):
        return int(value) % 2**bit

    def clamp_size(self, out, other):
        other = self.check_other(other)
        bits = self.bits if self.bits > other.bits else other.bits
        return UInt(bits, self.clamp(out, bits))

    def rm_bits(self, value):
        if value >= 2 ** self.bits:
            value = bin(self.clamp(value, self.bits))
            return int(value[-self.bits:], 2)
        else:
            return value

    def check_other(self, other):
        if type(other) != type(self):
            return UInt(self.bits, int(other))
        else:
            return other

    # Coercion Methods
    def __str__(self):
        return f'0b{self.value:0{self.bits}b}'

    def __index__(self):
        return self.value

    def __repr__(self):
        if self.value >= 0:
            return f'0x{self.value:0{self.bits//4}X}'

    # Math Functions
    def __add__(self, other):
        other = self.check_other(other)
        out = self.value + other.value
        return self.clamp_size(out, other)

    def __sub__(self, other):
        other = self.check_other(other)
        out = self.value - other.value
        return self.clamp_size(out, other)

    def __mul__(self, other):
        other = self.check_other(other)
        out = self.value * other.value
        return self.clamp_size(out, other)

    def __truediv__(self, other):
        other = self.check_other(other)
        out = self.value // other.value
        return self.clamp_size(out, other)

    # Boolean Functions
    def __eq__(self, other):
        other = self.check_other(other)
        return self.value == other.value

    def __gt__(self, other):
        other = self.check_other(other)
        return self.value > other.value

    def __ge__(self, other):
        other = self.check_other(other)
        return self.value >= other.value

    #Unary Functions
    def __and__(self, other):
        other = self.check_other(other)
        out = self.value & other.value
        return self.clamp_size(out, other)

    def __xor__(self, other):
        other = self.check_other(other)
        out = self.value ^ other.value
        return self.clamp_size(out, other)

    def __or__(self, other):
        other = self.check_other(other)
        out = self.value | other.value
        return self.clamp_size(out, other)

    def __invert__(self):
        return UInt(self.bits, self.clamp(~self.value, self.bits))

    def __rshift__(self, other):
        other = self.check_other(other)
        out = self.value >> other.value
        return UInt(self.bits, out)

    def __lshift__(self, other):
        other = self.check_other(other)
        out = self.rm_bits(self.value << other.value)
        return UInt(self.bits, out)

class SInt:
    def __init__(self, bits, value):
        if 65 > bits > 0:
            self.bits = bits
        elif bits > 64:
            self.bits = 64
        else:
            self.bits = 1

        self.value = self.clamp(value, self.bits)

    # Helper Functions
    def clamp(self, value, bits):
        value = int(value)
        if value % (2 ** bits) < 2 ** (bits - 1):
            value %= 2 ** bits
        else:
            value %= -2 ** bits

        return value

    def clamp_size(self, out, other):
        other = self.check_other(other)
        bits = self.bits if self.bits > other.bits else other.bits
        return SInt(bits, self.clamp(out, bits))

    def rm_bits(self, value):
        if value >= 2 ** (self.bits-1):
            value = bin(self.clamp(value, self.bits))
            return int(value[-self.bits:], 2)
        else:
            return value

    def check_other(self, other):
        if type(other) != type(self):
            return SInt(self.bits, int(other))
        else:
            return other

    # Coercion Methods
    def __str__(self):
        if self.value >= 0:
            return f'0b{self.value:0{self.bits}b}'
        else:
            return f'-0b{-self.value:0{self.bits}b}'

    def __index__(self):
        return self.value

    def __repr__(self):
        if self.value >= 0:
            return f'0x{self.value:0{self.bits//4}X}'
        else:
            return f'-0x{-self.value:0{self.bits//4}X}'

    # Math Functions
    def __add__(self, other):
        other = self.check_other(other)
        out = self.value + other.value
        return self.clamp_size(out, other)

    def __sub__(self, other):
        other = self.check_other(other)
        out = self.value - other.value
        return self.clamp_size(out, other)

    def __mul__(self, other):
        other = self.check_other(other)
        out = self.value * other.value
        return self.clamp_size(out, other)

    def __truediv__(self, other):
        other = self.check_other(other)
        out = self.value // other.value
        return self.clamp_size(out, other)

    # Boolean Functions
    def __eq__(self, other):
        other = self.check_other(other)
        return self.value == other.value

    def __gt__(self, other):
        other = self.check_other(other)
        return self.value > other.value

    def __ge__(self, other):
        other = self.check_other(other)
        return self.value >= other.value

    #Unary Functions
    def __and__(self, other):
        other = self.check_other(other)
        out = self.value & other.value
        return self.clamp_size(out, other)

    def __xor__(self, other):
        other = self.check_other(other)
        out = self.value ^ other.value
        return self.clamp_size(out, other)

    def __or__(self, other):
        other = self.check_other(other)
        out = self.value | other.value
        return self.clamp_size(out, other)

    def __invert__(self):
        return SInt(self.bits, self.clamp(~self.value, self.bits))

    def __neg__(self):
        return self.clamp(-self.value, self.bits)

    def __rshift__(self, other):
        other = self.check_other(other)
        out = self.value >> other.value
        return SInt(self.bits, out)

    def __lshift__(self, other):
        other = self.check_other(other)
        out = self.rm_bits(self.value << other.value)
        return SInt(self.bits, out)
