from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAType12 = recordclass('BSAType12', [
    'f_00',
    'eepk_type',
    'skill_id',
    'i_12',
    'f_16',
])


# Type 12
class Type12(BaseType):
    type = 12
    bsa_record = BSAType12
    byte_order = 'fIIIf'
    size = 20

    def __init__(self, index):
        super().__init__(index)
