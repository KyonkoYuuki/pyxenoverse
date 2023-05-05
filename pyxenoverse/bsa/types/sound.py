from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSASound = recordclass('BSASound', [
    'acb_file',
    'i_02',
    'cue_id',
    'i_06'
])


# Type 7
class Sound(BaseType):
    type = 7
    bsa_record = BSASound
    byte_order = 'HHHH'
    size = 8

    description_type = "acb_file"
    description = {
        0x0: "CAR_BTL_CMN",
        0x3: "Skill SE",

    }

    def __init__(self, index):
        super().__init__(index)
