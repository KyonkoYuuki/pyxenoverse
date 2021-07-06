from recordclass import recordclass

from pyxenoverse.bdm.subentry import BaseType

BDMType1 = recordclass('BDMType1', [
    'damage_type',
    'secondary_type',
    'damage_amount',
    'damage_special',
    'sound_type',
    'sound_id',
    'effect_1_eepk_id',
    'effect_1_skill_id',
    'effect_1_skill_type',
    'effect_2_eepk_id',
    'effect_2_skill_id',
    'effect_2_skill_type',
    'pushback_speed',
    'pushback_acceleration_percent',
    'user_stun',
    'victim_stun',
    'knockback_duration',
    'knockback_ground_impact_time',
    'knockback_recovery_after_impact_time',
    'knockback_gravity_time',
    'knockback_strength_x',
    'knockback_strength_y',
    'knockback_strength_z',
    'knockback_drag_y',
    'victim_invincibility_time',
    'ailment_type',
    'camera_shake_type',
    'camera_shake_time',
    'user_screen_flash_transparency',
    'victim_screen_flash_transparency',
    'transformation_type',
    'stumble_type',
    'I_02',
    'I_06',
    'F_08',
    'I_22',
    'I_30',
    'I_50',
    'I_68',
    'I_74',
    'I_80_1',
    'I_80_2',
    'I_80_3',
    'I_88_1',
    'I_88_2',
    'I_104',
])


class Type1(BaseType):
    bac_record = BDMType1
    byte_order = 'HHHHfHhhhhHhhhHffHHHHHHffffHHhHHhHHHHHHHHHHhhh'
    size = 108
