from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACOpponentKnockback = recordclass('BACOpponentKnockback', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'tracking',
    'u_0c',
    'u_0e'
])


# Type 5
class OpponentKnockback(BaseType):
    type = 5
    bac_record = BACOpponentKnockback
    byte_order = 'HHHHfHH'
    size = 16

    def __init__(self, index):
        super().__init__(index)
