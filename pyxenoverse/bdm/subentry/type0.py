from recordclass import recordclass

from pyxenoverse.bdm.subentry import BaseType

BDMType0 = recordclass('BDMType0', [
    'damage_type',
    'u_02',
    'damage_amount', #good
    'u_06',
    'f_08',
    'sound_type', #good1
    'sound_id',
    'effect_1_eepk_id',
    'effect_1_skill_id',
    'effect_1_skill_type',
    'u_16',
    'effect_2_eepk_id',
    'effect_2_skill_id',
    'effect_2_skill_type',
    'u_1e',
    'effect_3_eepk_id',
    'effect_3_skill_id',
    'effect_3_skill_type',
    'u_26',
    'pushback_speed',
    'pushback_acceleration_percent',
    'user_stun',
    'victim_stun',
    'knockback_duration',
    'knockback_recovery_after_impact_time',
    'knockback_ground_impact_time',
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
    'u_58_1', #array
    'u_58_2',
    'u_58_3',
    'damage_special',
    'u_60_1', #array
    'u_60_2',
    'stumble_type',
    'secondary_type',
    'camera_shake_type',
    'camera_shake_time',
    'user_screen_flash_transparency',
    'victim_screen_flash_transparency',
    'stamina_broken_bdm_id_override',
    'time_before_z_vanish_enabled',
    'user_animation_time',
    'victim_animation_time',
    'user_animation_speed',
    'victim_animation_speed'
])


class Type0(BaseType):
    bac_record = BDMType0
    byte_order = 'HHHHfHhhhHHhhHHhhHHffHHHHHHffffHHhHHhHHHHHHHHHHhhhHHHff'
    size = 128

    def convert_type1_to_type0(self, type1):
        self.data = self.bac_record(*([0] * len(self.bac_record.__fields__)))
        for field in type1.__fields__:
            if field in self.__fields__:
                self.data[field] = type1[field]

