from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAType10 = recordclass('BSAType10', [
    'skill_id',
    'i_02',
    'i_04'
])


# Type 10
class Type10(BaseType):
    type = 10
    bsa_record = BSAType10
    byte_order = 'IHH'
    size = 8

    def __init__(self, index):
        super().__init__(index)
