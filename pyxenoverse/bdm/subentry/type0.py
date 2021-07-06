from recordclass import recordclass

from pyxenoverse.bdm.subentry import BaseType

BDMType0 = recordclass('BDMType0', [
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
    'effect_3_eepk_id',
    'effect_3_skill_id',
    'effect_3_skill_type',
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
    'stamina_broken_bdm_id_override',
    'time_before_z_vanish_enabled',
    'user_animation_time',
    'victim_animation_time',
    'user_animation_speed',
    'victim_animation_speed',
    'transformation_type',
    'stumble_type',
    'u_02',
    'u_06',
    'f_08',
    'u_22',
    'u_30',
    'u_38',
    'u_58',
    'u_76',
    'u_82',
    'u_88_1', #array
    'u_88_2',
    'u_88_3',
    'u_96_1',#array
    'u_96_2'
])


class Type0(BaseType):
    bac_record = BDMType0
    byte_order = 'HHHHfHhhhHHhhHHhhHHffHHHHHHffffHHhHHhHHHHHHHHHHhhhHHHfI'
    size = 128

    def convert_type1_to_type0(self, type1):
        self.data = self.bac_record(*([0] * len(self.bac_record.__fields__)))
        for field in type1.__fields__:
            if field in self.__fields__:
                self.data[field] = type1[field]

