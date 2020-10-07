from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSASound = recordclass('BSASound', [
    'acb_file',
    'i_02',
    'cue_id',
    'i_06'
])


# Type 7
class Sound(BaseType):
    type = 7
    bac_record = BSASound
    byte_order = 'HHHH'
    size = 8

    def __init__(self, index):
        super().__init__(index)
