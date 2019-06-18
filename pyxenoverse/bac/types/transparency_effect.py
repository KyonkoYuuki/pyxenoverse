from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACTransparencyEffect = recordclass('BACTransparencyEffect', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'transparency_flags',
    'dilution',
    'u_0e',
    'u_10',
    'red',
    'green',
    'blue',
    'f_20',
    'f_24',
    'f_28',
    'f_2c',
    'f_30',
    'f_34',
    'f_38',
    'f_3c'
])


# Type 23
class TransparencyEffect(BaseType):
    type = 23
    bac_record = BACTransparencyEffect
    byte_order = 'HHHHIHHIfffffffffff'
    size = 64

    def __init__(self, index):
        super().__init__(index)
