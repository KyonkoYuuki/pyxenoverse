from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAEntryPassing = recordclass('BSAEntryPassing', [
    'i_00',
    'main_condition',
    'bsa_entry',
    'i_06',
    'bac_condition',
    'f_12'
])


# Type 0
class EntryPassing(BaseType):
    type = 0
    bac_record = BSAEntryPassing
    byte_order = 'HHHHff'
    size = 16

    def __init__(self, index):
        super().__init__(index)
