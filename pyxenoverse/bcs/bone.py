import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name

BCSBone = recordclass('BCSBone', [
    'u_00',
    'u_04',
    'u_08',
    'u_0c',
    'u_0e',
    'u_10',
    'u_12',
    'u_14',
    'u_16',
    'u_18',
    'u_1a',
    'u_1c',
    'u_1e',
    'u_20',
    'u_22',
    'u_24',
    'u_26',
    'u_28',
    'u_2a',
    'u_2c',
    'u_2e',
    'name_offset'
])
BCS_BONE_SIZE = 52
BCS_BONE_BYTE_ORDER = 'IIIHHHHHHHHHHHHHHHHHHI'


class Bone(BaseRecord):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.data = BCSBone(*([0] * len(BCSBone.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSBone(*struct.unpack(endian + BCS_BONE_BYTE_ORDER, f.read(BCS_BONE_SIZE)))
        if self.name_offset:
            self.name = read_name(f, address + self.name_offset)
            # print(self.name)
        # print(self.data)

    def write(self, f, names, endian):
        address = f.tell()
        self.name_offset = 0
        f.write(struct.pack(endian + BCS_BONE_BYTE_ORDER, *self.data))

        # Add name
        if self.name:
            names.append((address, 0x30, self.name))

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSBone(*other.data)
        self.name = other.name
        return True
