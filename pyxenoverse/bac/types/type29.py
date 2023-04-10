from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType29 = recordclass('BACType29', [
    'start_time',
    'duration',
    'u_04',
    'character_type',

    'part_flags',
    'u_12',
    'glare_red_start',
    'glare_green_start',
    'glare_blue_start',
    'glare_alpha_start',
    'glare_red_end',
    'glare_green_end',
    'glare_blue_end',
    'glare_alpha_end',
    'f_48',
    'u_52',
    'u_56'
])


# Type 29
class Type29(BaseType):
    type = 29
    bac_record = BACType29
    byte_order = 'HHHH II fffffffff II'
    size = 60

    def __init__(self, index):
        super().__init__(index)
