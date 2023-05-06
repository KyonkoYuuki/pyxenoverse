from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAHitbox = recordclass('BSAHitbox', [
    'matrix_flags',
    'i_02',
    'i_04',
    'i_06',
    'position_x',
    'position_y',
    'position_z',
    'hitbox_scale',
    'max_box_x',
    'max_box_y',
    'max_box_z',
    'min_box_x',
    'min_box_y',
    'min_box_z',
    'amount',
    'power',

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
    byte_order = 'HHHH ffff ffff ff HHHH HHHH'
    size = 64

    def __init__(self, index):
        super().__init__(index)
