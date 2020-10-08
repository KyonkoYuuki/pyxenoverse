from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACPhysics = recordclass('BACPhysics', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'function_type',
    'ean_index',
    'u_10',
    'f_14',
    'f_18',
    'u_1c'
])


# Type 18
class Physics(BaseType):
    type = 18
    bac_record = BACPhysics
    byte_order = 'HHHHIIIffI'
    size = 32

    def __init__(self, index):
        super().__init__(index)
