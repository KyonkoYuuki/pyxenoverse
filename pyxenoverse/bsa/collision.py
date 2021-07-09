import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord

BSACollision = recordclass('BSACollision', [
    'eepk_type',
    'skill_id',
    'effect_id',
    'i_08',
    'i_12',
    'i_16',
    'i_20',
])

BSA_COLLISION_SIZE = 24

BSA_COLLISION_BYTE_ORDER = 'HHIIIII'


class Collision(BaseRecord):
    type = -2
    bsa_record = BSACollision

    def __init__(self):
        super().__init__()
        self.data = BSACollision(*([0] * len(BSACollision.__fields__)))

    def read(self, f, endian):
        self.data = BSACollision(*struct.unpack(endian + BSA_COLLISION_BYTE_ORDER, f.read(BSA_COLLISION_SIZE)))
        # print(self.data)

    def write(self, f, endian):
        f.write(struct.pack(endian + BSA_COLLISION_BYTE_ORDER, *self.data))

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BSACollision(*other.data)
        return True
