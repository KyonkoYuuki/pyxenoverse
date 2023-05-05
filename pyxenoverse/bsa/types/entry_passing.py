from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAEntryPassing = recordclass('BSAEntryPassing', [
    'i_00',
    'main_condition',
    'bsa_entry_id',
    'jump_to_bac_entry_id',
    'bac_condition',
    'f_12'
])


# Type 0
class EntryPassing(BaseType):
    type = 0
    bsa_record = BSAEntryPassing
    byte_order = 'HHHHff'
    size = 16

    def __init__(self, index):
        super().__init__(index)
