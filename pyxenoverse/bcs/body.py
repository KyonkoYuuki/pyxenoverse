import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bcs.bone_scale import BoneScale, BCS_BONE_SCALE_SIZE

BCSBody = recordclass('BCSBody', [
    'u_00',
    'num',
    'bone_scale_offset'
])
BCS_BODY_SIZE = 8
BCS_BODY_BYTE_ORDER = 'HHI'


class Body(BaseRecord):
    def __init__(self):
        super().__init__()
        self.bone_scales = []
        self.data = BCSBody(*([0] * len(BCSBody.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSBody(*struct.unpack(endian + BCS_BODY_BYTE_ORDER, f.read(BCS_BODY_SIZE)))
        # print(self.data)
        self.bone_scales.clear()
        for i in range(self.num):
            f.seek(address + self.bone_scale_offset + i * BCS_BONE_SCALE_SIZE)
            bone_scale = BoneScale()
            bone_scale.read(f, endian)
            self.bone_scales.append(bone_scale)

    def write(self, f, bone_scales, endian):
        address = f.tell()
        self.num = len(self.bone_scales)
        self.bone_scale_offset = 0
        f.write(struct.pack(endian + BCS_BODY_BYTE_ORDER, *self.data))

        # Add bone scales
        if self.num:
            bone_scales.append((address, 0x4, self.bone_scales))

        return f.tell()

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSBody(*other.data)
        self.bone_scales = other.bone_scales.copy()
        return True
