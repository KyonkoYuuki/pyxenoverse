from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAType8 = recordclass('BSAType8', [
    'i_00',
    'i_04',
    'i_08',
    'i_12',
    'i_16',
    'i_20'
])


# Type 8
class Type8(BaseType):
    type = 8
    bac_record = BSAType8
    byte_order = 'IIIIII'
    size = 24

    def __init__(self, index):
        super().__init__(index)
