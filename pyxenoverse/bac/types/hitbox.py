from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACHitbox = recordclass('BACHitbox', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'bdm_entry',
    'hitbox_flags',
    'damage',
    'damage_when_blocked',
    'stamina_taken_when_blocked',
    'use_matrix',
    'bdm_type',
    'u_14',
    'f_18',
    'position_x',
    'position_y',
    'position_z',
    'size_x',
    'size_y',
    'size_z',
    'rotation_x',
    'rotation_y',
    'rotation_z'
])


# Type 1
class Hitbox(BaseType):
    type = 1
    bac_record = BACHitbox
    byte_order = 'HHHHHHHHHBBIffffffffff'
    size = 64
    dependencies = {
        ('bdm_entry', 'bdm_type'): {0x1: 'Character', 0x2: 'Skill'}
    }

    bdm_type_dict = {0x0 : "CMN",
                     0x1 : "Character",
                     0x2 : "Skill"}

    def __init__(self, index):
        super().__init__(index)
