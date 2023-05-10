from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSADeflection = recordclass('BSADeflection', [
    'i_00',
    'i_04',
    'i_08',
    'f_12',
    'f_16',
    'f_20',
    'i_24',
    'i_28',
    'i_32',
    'i_36',
    'i_40',
    'i_44',
    'i_48',
    'newpower',
    'i_52',
    'i_54'
])


# Type 4
class Deflection(BaseType):
    type = 4
    bsa_record = BSADeflection
    byte_order = 'IIIfffIIIIIIHHHH'
    size = 56

    def __init__(self, index):
        super().__init__(index)
