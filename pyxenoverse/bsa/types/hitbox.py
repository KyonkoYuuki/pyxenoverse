from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAHitbox = recordclass('BSAHitbox', [
    'i_00',
    'i_02',
    'i_04',
    'i_06',
    'position_x',
    'position_y',
    'position_z',
    'hitbox_scale',
    'f_24',
    'f_28',
    'f_32',
    'f_36',
    'f_40',
    'amount',
    'lifetime',
    'i_50',
    'i_52',
    'i_54',
    'i_56',
    'bdm_first_hit_id',
    'bdm_multiple_hits_id',
    'bdm_last_hit_id'
])


# Type 3
class Hitbox(BaseType):
    type = 3
    bsa_record = BSAHitbox
    byte_order = 'HHHHffffffffffHHHHHHHH'
    size = 64

    def __init__(self, index):
        super().__init__(index)
