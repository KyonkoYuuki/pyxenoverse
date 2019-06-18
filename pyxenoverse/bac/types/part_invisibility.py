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

    def __init__(self, index):
        super().__init__(index)
