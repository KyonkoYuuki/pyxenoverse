from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAType13 = recordclass('BSAType13', [
    'i_00',
    'i_02',
    'power',
    'f_08',
    'i_12',
    'f_16',
    'i_20',
    'i_24',
    'i_28'
])


# Type 13
class Type13(BaseType):
    type = 13
    bsa_record = BSAType13
    byte_order = 'HH ff I f III'
    size = 32

    def __init__(self, index):
        super().__init__(index)
