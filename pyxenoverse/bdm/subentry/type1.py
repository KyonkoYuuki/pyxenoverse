from recordclass import recordclass

from pyxenoverse.bdm.subentry import BaseType

BDMType1 = recordclass('BDMType1', [
    'damage_type',
    'u_02', # Does this say if its a type 0 or 1?
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
    'knockback_ground_impact_time',
    'knockback_recovery_after_impact_time',
    'u_3a',
    'knockback_strength_x',
    'knockback_strength_y',
    'knockback_strength_z',
    'knockback_drag_y',
    'u_4c',
    'knockback_gravity_time',
    'victim_invincibility_time',
    'u_52',
    'transformation_type',
    'ailment_type',
    'u_58',
    'u_5a',
    'u_5c',
    'special',
    'u_60',
    'u_62',
    'stumble_type',
    'secondary_type',
    'camera_shake_type',
    'camera_shake_time',
    'user_screen_flash_transparency',
    'victim_screen_flash_transparency',
    'u_68',
    'u_6a'
])


class Type1(BaseType):
    bac_record = BDMType1
    byte_order = 'HHHHfhhhhhHhhhHffHHHHHHffffHHHHHHHHHHHHHHhHhhHH'
    size = 108
