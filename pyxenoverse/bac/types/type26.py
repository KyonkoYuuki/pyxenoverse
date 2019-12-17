from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACType26 = recordclass('BACType26', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'u_0c',
    'u_10',
    'u_14',
    'u_18',
    'u_1c',
    'u_20',
    'u_24',
    'u_28',
    'u_2c',
    'u_30',
    'u_34',
    'u_38',
    'u_3c',
    'u_40',
    'u_44',
    'u_48',
    'u_4c',
])


# Type 26
class Type26(BaseType):
    type = 26
    bac_record = BACType26
    byte_order = 'HHHHIIIIIIIIIIIIIIIIII'
    size = 80

    def __init__(self, index):
        super().__init__(index)
