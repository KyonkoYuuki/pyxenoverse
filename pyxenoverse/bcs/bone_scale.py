import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name

BCSBoneScale = recordclass('BCSBoneScale', [
    'x',
    'y',
    'z',
    'name_offset'
])
BCS_BONE_SCALE_SIZE = 16
BCS_BONE_SCALE_BYTE_ORDER = 'fffI'


class BoneScale(BaseRecord):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.data = BCSBoneScale(*([0] * len(BCSBoneScale.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSBoneScale(*struct.unpack(endian + BCS_BONE_SCALE_BYTE_ORDER, f.read(BCS_BONE_SCALE_SIZE)))
        if self.name_offset:
            self.name = read_name(f, address + self.name_offset)
            # print(self.name)
        # print(self.data)

    def write(self, f, names, endian):
        address = f.tell()
        self.name_offset = 0
        f.write(struct.pack(endian + BCS_BONE_SCALE_BYTE_ORDER, *self.data))

        # Add name
        if self.name:
            names.append((address, 0xc, self.name))
