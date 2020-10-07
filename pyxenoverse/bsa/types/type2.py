from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAType2 = recordclass('BSAType2', [
    'i_00',
    'i_02',
    'i_04',
    'i_06'
])


# Type 2
class Type2(BaseType):
    type = 2
    bac_record = BSAType2
    byte_order = 'HHHH'
    size = 8

    def __init__(self, index):
        super().__init__(index)
