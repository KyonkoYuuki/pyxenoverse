from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType18 = recordclass('BACType18', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'u_0c',
    'u_10',
    'f_14',
    'f_18',
    'u_1c'
])


# Type 18
class Type18(BaseType):
    type = 18
    bac_record = BACType18
    byte_order = 'HHHHIIIffI'
    size = 32

    def __init__(self, index):
        super().__init__(index)
