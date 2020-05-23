import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bcs.bone import Bone, BCS_BONE_SIZE

BCSSkeleton = recordclass('BCSSkeleton', [
    'u_00',
    'num',
    'bones_offset'
])
BCS_SKELETON_SIZE = 8
BCS_SKELETON_BYTE_ORDER = 'HHI'


class Skeleton(BaseRecord):
    def __init__(self):
        super().__init__()
        self.bones = []
        self.data = BCSSkeleton(*([0] * len(BCSSkeleton.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSSkeleton(*struct.unpack(endian + BCS_SKELETON_BYTE_ORDER, f.read(BCS_SKELETON_SIZE)))
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
        f.write(struct.pack(endian + BCS_SKELETON_BYTE_ORDER, *self.data))
        for bone in self.bones:
            bone.write(f, names, endian)
        return f.tell()

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSSkeleton(*other.data)
        self.bones = other.bones.copy()
        return True

