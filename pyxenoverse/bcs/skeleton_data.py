import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bcs.bone import Bone, BCS_BONE_SIZE

BCSSkeletonData = recordclass('BCSSkeletonData', [
    'u_00',
    'num',
    'bones_offset'
])
BCS_SKELETON_DATA_SIZE = 8
BCS_SKELETON_DATA_BYTE_ORDER = 'HHI'


class SkeletonData(BaseRecord):
    def __init__(self):
        super().__init__()
        self.bones = []
        self.data = BCSSkeletonData(*([0] * len(BCSSkeletonData.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSSkeletonData(*struct.unpack(endian + BCS_SKELETON_DATA_BYTE_ORDER, f.read(BCS_SKELETON_DATA_SIZE)))
        # print(self.data)
        self.bones.clear()
        for i in range(self.num):
            f.seek(address + self.bones_offset + i * BCS_BONE_SIZE)
            bone = Bone()
            bone.read(f, endian)
            self.bones.append(bone)

    def write(self, f, names, endian):
        self.num = len(self.bones)
        self.bones_offset = 0x8 if self.num else 0  # offset is always 0x8
        f.write(struct.pack(endian + BCS_SKELETON_DATA_BYTE_ORDER, *self.data))
        for bone in self.bones:
            bone.write(f, names, endian)
        return f.tell()

