#!/usr/bin/python3
import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, merge_dict
from pyxenoverse.bac.types.animation import Animation
from pyxenoverse.bac.types.hitbox import Hitbox
from pyxenoverse.bac.types.acceleration_movement import AccelerationMovement
from pyxenoverse.bac.types.invulnerability import Invulnerability
from pyxenoverse.bac.types.motion_adjust import MotionAdjust
from pyxenoverse.bac.types.opponent_knockback import OpponentKnockback
from pyxenoverse.bac.types.chain_attack_parameters import ChainAttackParameters
from pyxenoverse.bac.types.bcm_callback import BcmCallback
from pyxenoverse.bac.types.effect import Effect
from pyxenoverse.bac.types.projectile import Projectile
from pyxenoverse.bac.types.camera import Camera
from pyxenoverse.bac.types.sound import Sound
from pyxenoverse.bac.types.targeting_assistance import TargetingAssistance
from pyxenoverse.bac.types.part_invisibility import PartInvisibility
from pyxenoverse.bac.types.animation_modification import AnimationModification
from pyxenoverse.bac.types.transform_control import TransformControl
from pyxenoverse.bac.types.screen_effect import ScreenEffect
from pyxenoverse.bac.types.throw_handler import ThrowHandler
from pyxenoverse.bac.types.physics import Physics
from pyxenoverse.bac.types.aura_effect import AuraEffect
from pyxenoverse.bac.types.homing_movement import HomingMovement
from pyxenoverse.bac.types.eye_movement import EyeMovement
from pyxenoverse.bac.types.type22 import Type22
from pyxenoverse.bac.types.transparency_effect import TransparencyEffect
from pyxenoverse.bac.types.dual_skill_data import DualSkillData
from pyxenoverse.bac.types.charge_attack_parameters import ChargeAttackParameters
from pyxenoverse.bac.types.extended_camera_control import ExtendedCameraControl
from pyxenoverse.bac.types.effect_property_control import EffectPropertyControl

ITEM_TYPES = {
    0: Animation,
    1: Hitbox,
    2: AccelerationMovement,
    3: Invulnerability,
    4: MotionAdjust,
    5: OpponentKnockback,
    6: ChainAttackParameters,
    7: BcmCallback,
    8: Effect,
    9: Projectile,
    10: Camera,
    11: Sound,
    12: TargetingAssistance,
    13: PartInvisibility,
    14: AnimationModification,
    15: TransformControl,
    16: ScreenEffect,
    17: ThrowHandler,
    18: Physics,
    19: AuraEffect,
    20: HomingMovement,
    21: EyeMovement,
    22: Type22,
    23: TransparencyEffect,
    24: DualSkillData,
    25: ChargeAttackParameters,
    26: ExtendedCameraControl,
    27: EffectPropertyControl,
}

BACSubEntry = recordclass('BACSubEntry', [
    'type',
    'num',
    'u_04',
    'offset',
    'u_0c'
])
BAC_SUB_ENTRY_SIZE = 16
BAC_SUB_ENTRY_BYTE_ORDER = 'HHIII'


class SubEntry(BaseRecord):
    def __init__(self, index):
        super().__init__()
        self.items = []
        self.index = index
        self.data = BACSubEntry(*([0] * len(BACSubEntry.__fields__)))
        self.dependencies = {}

    def read(self, f, endian):
        self.data = BACSubEntry(*struct.unpack(endian + BAC_SUB_ENTRY_BYTE_ORDER, f.read(BAC_SUB_ENTRY_SIZE)))
        # print(f'offset={f.tell()}, type={self.type}, num={self.num}')
        if self.type not in ITEM_TYPES:
            return

    def read_items(self, f, endian, type17_small):
        for i in range(self.num):
            item = ITEM_TYPES[self.type](i)
            item_offset = self.offset + item.get_size(type17_small) * i
            # print("{}: {}".format(item.__class__.__name__, item_offset))
            f.seek(item_offset)
            item.read(f, endian, type17_small)
            self.items.append(item)

    def write(self, f, item_offset, endian):
        self.items.sort(key=lambda n: n.start_time)
        self.num = len(self.items)
        if self.items:
            self.offset = item_offset
        else:
            self.offset = 0
        f.write(struct.pack(endian + BAC_SUB_ENTRY_BYTE_ORDER, *self.data))
        # print("{}: {}".format(self.item_types[self.type].__name__, self.num))
        for i, item in enumerate(self.items):
            f.seek(item_offset)
            item.write(f, endian)
            # print("{}: {}".format(item.__class__.__name__, item_offset))
            item_offset += item.get_size(type17_small=False)
        return item_offset

    def paste(self, other, changed_values={}, copy_items=True):
        if type(self) != type(other):
            return False
        if self.type != other.type:
            return False
        self.data = BACSubEntry(*other.data)
        if copy_items:
            self.items = other.items.copy()
            for item in self.items:
                item.replace_values(changed_values)
        return True

    def get_readable_name(self):
        return ITEM_TYPES[self.type].__name__ + ' Group'

    def get_type_name(self):
        return ITEM_TYPES[self.type].__name__

    def get_static_values(self):
        static_values = {}
        for item in self.items:
            merge_dict(static_values, item.get_static_values())
        return static_values
