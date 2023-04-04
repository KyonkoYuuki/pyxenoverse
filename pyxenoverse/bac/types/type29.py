from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType29 = recordclass('BACType29', [
    'start_time',
    'duration',
    'u_04',
    'character_type',

    'u_08',
    'u_12',
    'f_16',
    'f_20',
    'f_24',
    'f_28',
    'f_32',
    'f_36',
    'f_40',
    'f_44',
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
