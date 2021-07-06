from recordclass import recordclass

from pyxenoverse.bdm.subentry import BaseType

BDMType1 = recordclass('BDMType1', [
    'damage_type',
    'u_02',
    'damage_amount',
    'u_06',
    'f_08',
    'sound_type',
    'sound_id',
    'effect_1_eepk_id',
    'effect_1_skill_id',
    'effect_1_skill_type',
    'u_16',
    'effect_2_eepk_id',
    'effect_2_skill_id',
    'effect_2_skill_type',
    'u_1e',
    'pushback_speed',
    'pushback_acceleration_percent',
    'user_stun',
    'victim_stun',
    'knockback_duration',
    'knockback_recovery_after_impact_time',
    'knockback_ground_impact_time',
    'u_32',
    'knockback_strength_x',
    'knockback_strength_y',
    'knockback_strength_z',
    'knockback_drag_y',
    'u_44',
    'knockback_gravity_time',
    'victim_invincibility_time',
    'u_4a',
    'transformation_type',
    'ailment_type',
    'u_50_1',#array
    'u_50_2',#array
    'u_50_3',#array
    'damage_special',
    'u_58_1',#array
    'u_58_2',#array
    'stumble_type',
    'secondary_type',
    'camera_shake_type',
    'camera_shake_time',
    'user_screen_flash_transparency',
    'victim_screen_flash_transparency',
    'u_68'
])


class Type1(BaseType):
    bac_record = BDMType1
    byte_order = 'HHHHfHhhhhHhhhHffHHHHHHffffHHhHHhHHHHHHHHHHhhh'
    size = 108
