from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACEffect = recordclass('BACEffect', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'type',
    'bone_link',
    'skill_id',
    'use_skill_id',
    'effect_id',
    'u_14',
    'u_18',
    'u_1c',
    'u_20',
    'u_24',
    'u_28',
    'on_off_switch'
])


# Type 8
class Effect(BaseType):
    type = 8
    bac_record = BACEffect
    byte_order = 'HHHHHHHHIIIIIIII'
    size = 48
    dependencies = {
        ('skill_id', 'use_skill_id'): {0x0: 'Yes'}
    }

    def __init__(self, index):
        super().__init__(index)
