from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAEffect = recordclass('BSAEffect', [
    'eepk_type',
    'skill_id',
    'effect_id',
    'i_06',
    'effect_switch',
    'i_10',
    'position_x',
    'position_y',
    'position_z'
])


# Type 6
class Effect(BaseType):
    type = 6
    bsa_record = BSAEffect
    byte_order = 'HHHHHHfff'
    size = 24

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
