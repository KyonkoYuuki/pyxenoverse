from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType22 = recordclass('BACType22', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'f_0c'
])


# Type 22
class Type22(BaseType):
    type = 22
    bac_record = BACType22
    byte_order = 'HHHHIf'
    size = 16

    def __init__(self, index):
        super().__init__(index)
