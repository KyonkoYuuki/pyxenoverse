import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name

BCSBone = recordclass('BCSBone', [
    'u_00',
    'u_04',
    'u_08',
    'f_0c',
    'f_0e',
    'f_10',
    'f_12',
    'f_14',
    'f_16',
    'f_18',
    'f_1a',
    'f_1c',
    'f_1e',
    'f_20',
    'f_22',
    'f_24',
    'f_26',
    'f_28',
    'f_2a',
    'f_2c',
    'f_2e',
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
