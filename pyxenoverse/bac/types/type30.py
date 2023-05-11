from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType30 = recordclass('BACType30', [
    'start_time',
    'duration',
    'u_04',
    'character_type',

    'type30_duration',
    'u_12',
    'u_16',
    'u_20',
    'u_24',

    'u_28',
    'u_32',
    'u_36',
    'u_40',

    'u_44',



])


# Type 30
class Type30(BaseType):
    type = 30
    bac_record = BACType30
    byte_order = 'HHHH f IIII IIII I'
    size = 48

    def __init__(self, index):
        super().__init__(index)
