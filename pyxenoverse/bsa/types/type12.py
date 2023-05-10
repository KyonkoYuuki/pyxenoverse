from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAType12 = recordclass('BSAType12', [
    'effect_id',
    'eepk_type',
    'skill_id',
    'i_12',
    'f_16',
])


# Type 12
class Type12(BaseType):
    type = 12
    bsa_record = BSAType12
    byte_order = 'fIIIf'
    size = 20


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

    def __init__(self, index):
        super().__init__(index)
