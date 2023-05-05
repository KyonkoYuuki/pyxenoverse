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


    description_type = "eepk_type"
    description = {
        0x0: "Global",
        0x1: "Stage BG",
        0x2: "Player",
        0x3: "Skill",
        0x5: "Super",
        0x6: "Ultimate",
        0x7: "Evasive",
        0x8: "Unknown (0x8)",
        0x9: "Ki blast",
        0xa: "Unknown (0xa)",
        0xb: "Stage (0xb)",
        0xc: "Awoken"
    }


    def __init__(self):
        super().__init__()
        self.data = BSACollision(*([0] * len(BSACollision.__fields__)))

    def read(self, f, endian):
        self.data = BSACollision(*struct.unpack(endian + BSA_COLLISION_BYTE_ORDER, f.read(BSA_COLLISION_SIZE)))
        # print(self.data)

    @classmethod
    def description_choices(cls):
        return {v: k for k, v in cls.description.items()}

    def write(self, f, endian):
        f.write(struct.pack(endian + BSA_COLLISION_BYTE_ORDER, *self.data))

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BSACollision(*other.data)
        return True
