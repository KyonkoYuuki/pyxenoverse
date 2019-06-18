from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACSound = recordclass('BACSound', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'acb_type',
    'u_0a',
    'cue_id',
    'u_0e'
])


# Type 11
class Sound(BaseType):
    type = 11
    bac_record = BACSound
    byte_order = 'HHHHHHHH'
    size = 16

    def __init__(self, index):
        super().__init__(index)
