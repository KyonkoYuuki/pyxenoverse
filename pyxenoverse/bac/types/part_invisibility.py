from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACPartInvisibility = recordclass('BACPartInvisibility', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'bcs_part_id',
    'on_off_switch'
])


# Type 13
class PartInvisibility(BaseType):
    type = 13
    bac_record = BACPartInvisibility
    byte_order = 'HHHHHH'
    size = 12
    description_type = "bcs_part_id"
    description = {0x0: "Face base",
                   0x1: "Face forehead",
                   0x2: "Face eye",
                   0x3: "Face nose",
                   0x4: "Face ear",
                   0x5: "Hair",
                   0x6: "Bust",
                   0x7: "Pants",
                   0x8: "Rist",
                   0x9: "Boots",
                   0x1: "Face forehead"}

    def __init__(self, index):
        super().__init__(index)
