from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACSound = recordclass('BACSound', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'acb_type',
    'sound_flags',
    'cue_id',
    'u_0e'
])


# Type 11
class Sound(BaseType):
    type = 11
    bac_record = BACSound
    byte_order = 'HHHHHHHH'
    size = 16

    description_type = "acb_type"
    description = {
        0x0: "CAR_BTL_CMN",
        0x1: "Unknown (0x1)",
        0x2: "Character SE",
        0x3: "Character VOX",
        0x4: "Unknown (0x4)",
        0x5: "Unknown (0x5)",
        0x6: "Unknown (0x6)",
        0x7: "Unknown (0x7)",
        0x8: "Unknown (0x8)",
        0xa: "Skill SE",
        0xb: "Skill VOX",
        0x16: "Unknown (0x16)",
        0x17: "Unknown (0x17)",
        0x1a: "Unknown (0x1a)",
        0x1c: "Unknown (0x1c)",
        0x1d: "Unknown (0x1d)",
        0x22: "Unknown (0x22)",
        0x23: "Unknown (0x23)",
        0x34: "Unknown (0x34)",
        0x35: "Unknown (0x35)",
        0x37: "Unknown (0x37)",
        0x39: "Unknown (0x39)",
        0x62: "Unknown (0x62)",
        0x100: "Unknown (0x100)",
    }

    def __init__(self, index):
        super().__init__(index)
