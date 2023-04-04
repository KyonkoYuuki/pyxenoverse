from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType28 = recordclass('BACType28', [
    'start_time',
    'duration',
    'u_04',
    'character_type',

    'u_00',
    'u_040',
    'u_08',
    'u_12',
    'u_16',
    'u_20',
    'u_24'
])


# Type 28
class Type28(BaseType):
    type = 28
    bac_record = BACType28
    byte_order = 'HHHH IIIIIII'
    size = 36

    def __init__(self, index):
        super().__init__(index)
