# ---------- Part 1 ------------- #
# We now need to parse the hierarchy of packets.

from dataclasses import dataclass
import functools 
import operator

INPUT = "220D69802BE00A0803711E1441B1006E39C318A12730C200DCE66D2CCE360FA0055652CD32966E3004677EDF600B0803B1361741510076254138D8A00E4FFF3E3393ABE4FC7AC10410010799D2A4430003764DBE281802F3102CA00D4840198430EE0E00021D04E3F41F84AE0154DFDE65A17CCBFAFA14ADA56854FE5E3FD5BCC53B0D2598027A00848C63F2B918C7E513DEC3290051B3867E009CCC5FE46BD520007FE5E8AD344B37583D0803E40085475887144C01A8C10FE2B9803B0720D45A3004652FD8FA05F80122CAF91E5F50E66BEF8AB000BB0F4802039C20917B920B9221200ABF0017B9C92CCDC76BD3A8C4012CCB13CB22CDB243E9C3D2002067440400D9BE62DAC4D2DC0249BF76B6F72BE459B279F759AE7BE42E0058801CC059B08018A0070012CEC045BA01006C03A8000D46C02FA000A8EA007200800E00618018E00410034220061801D36BF178C01796FC52B4017100763547E86000084C7E8910AC0027E9B029FE2F4952F96D81B34C8400C24AA8CDAF4F1E98027C00FACDE3BA86982570D13AA640195CD67B046F004662711E989C468C01F1007A10C4C8320008742287117C401A8C715A3FC2C8EB3777540048272DFE7DE1C0149AC8BC9E79D63200B674013978E8BE5E3A2E9AA3CCDD538C01193CFAB0A146006AA00087C3E88B130401D8E304A239802F39FAC922C0169EA3248DF2D600247C89BCDFE9CA7FFD8BB49686236C9FF9795D80C0139BEC4D6C017978CF78C5EB981FCE7D4D801FA9FB63B14789534584010B5802F3467346D2C1D1E080355B00424FC99290C7E5D729586504803A2D005E677F868C271AA479CEEB131592EE5450043A932697E6A92C6E164991EFC4268F25A294600B5002A3393B31CC834B972804D2F3A4FD72B928E59219C9C771EC3DC89D1802135C9806802729694A6E723FD6134C0129A019E600"

class ListUtils:
    @classmethod
    def sum_list(cls, l):
        return sum(l)
    
    @classmethod
    def mult_list(cls, l):
        return functools.reduce(operator.mul, l)

    @classmethod
    def min_list(cls, l):
        return min(l)
    
    @classmethod
    def max_list(cls, l):
        return max(l)
    
    @classmethod
    def greater_than(cls, l):
        return int(l[0] > l[1])
    
    @classmethod
    def less_than(cls, l):
        return int(l[0] < l[1])
    
    @classmethod
    def equal_to(cls, l):
        return int(l[0] == l[1])
    
@dataclass
class Packet:
    version: int
    type: int
    
@dataclass
class LiteralPacket(Packet):
    value: int
    bin_length: str
    
    def __str__(self):
        return "A literal packet with version = {}, type = {}, value = {}".format(self.version, self.type, self.value)

@dataclass
class OperatorPacket(Packet):
    length_type: int
    length: int
    subpackets: list[LiteralPacket]        
    
    def has_ended(self):
        if self.length_type == 1:
            return len(self.subpackets) == self.length
        else:
            return sum([p.bin_length for p in self.subpackets]) == self.length

    @property
    def bin_length(self):
        if not self.has_ended():
            raise Exception("Packet has not ended")
            
        blength = 3 + 3 + 1 + \
            (15 if self.length_type == 0 else 11) + \
            sum([p.bin_length for p in self.subpackets])
        return blength
    
    def add_subpacket(self, packet):
        self.subpackets.append(packet)
        
    @property
    def value(self):
        if not self.has_ended():
            raise Exception("Packet has not ended")
        
        packet_values = [p.value for p in self.subpackets]
        op_func = {
            0: ListUtils.sum_list,
            1: ListUtils.mult_list,
            2: ListUtils.min_list,
            3: ListUtils.max_list,
            5: ListUtils.greater_than,
            6: ListUtils.less_than,
            7: ListUtils.equal_to            
        }
        return op_func[self.type](packet_values)
    
    def __str__(self):
        return "A operator packet with version = {}, type = {}, length_type = {}, length = {}".format(self.version, self.type, self.length_type, self.length)

 
# convert hex to binary
def hex_to_bin(hex_input):
    hb_table = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }
    out = "".join([hb_table[c] for c in hex_input])
    return out

def bin_to_dec(bin_input):
    return int(bin_input, 2)
    
input = hex_to_bin(INPUT)

def consume_input(size):
    global input
    consumed = input[:size]
    input = input[size:]
    return consumed

operator_stack = []
 
# DFS using stack, nodes are operator packets
while len(input) > 10:  # 11 (3 + 3 + 5) is the minimum size of a packet
    # start of a packet
    packet_version = bin_to_dec(consume_input(3))
    packet_type = bin_to_dec(consume_input(3))
    bin_length = 6
    if packet_type == 4:
        # Parse and create the literal packet
        literal_value = ""
        while True:
            five_bit_group = consume_input(5)
            bin_length += 5
            literal_value += five_bit_group[1:]
            if five_bit_group[0] == '0':
                break
            
        literal_value = bin_to_dec(literal_value)
        packet = LiteralPacket(packet_version, packet_type, literal_value, bin_length)
        if len(operator_stack) > 0:
            operator_stack[-1].add_subpacket(packet)
        else:
            operator_stack.append(packet)
    else:
        # Prase header and create operator packet
        length_type = int(consume_input(1))
        if length_type == 0:
            length = consume_input(15)
        else:
            length = consume_input(11)
        length = bin_to_dec(length)
        packet = OperatorPacket(packet_version, packet_type, length_type, length, [])
        operator_stack.append(packet)
        
    while len(operator_stack) > 1 and operator_stack[-1].has_ended():
        op = operator_stack.pop()
        operator_stack[-1].add_subpacket(op)
        
assert(len(operator_stack) == 1 and operator_stack[-1].has_ended())
print(operator_stack[-1].value)