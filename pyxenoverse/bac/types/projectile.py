from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACProjectile = recordclass('BACProjectile', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'skill_id',
    'can_use_cmn_bsa',
    'projectile_id',
    'bone_to_spawn_from',
    'spawn_source',
    'position_x',
    'position_y',
    'position_z',
    'skill_type',
    'spawn_properties',
    'f_28',
    'u_2c',
    'u_2e',
    'projectile_health',
    'u_34',
    'u_38',
    'u_3c'
])


# Type 9
class Projectile(BaseType):
    type = 9
    bac_record = BACProjectile
    byte_order = 'HHHHHHIHHfffIIfHHIIII'
    size = 64
    dependencies = {
        ('skill_id', None): {},
        ('projectile_id', 'can_use_cmn_bsa'): {0x0: 'Yes'}
    }

    def __init__(self, index):
        super().__init__(index)
