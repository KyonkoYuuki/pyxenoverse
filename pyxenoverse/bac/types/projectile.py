import struct
import math
from recordclass import recordclass
from pyxenoverse.bac.types import BaseType

BACProjectile = recordclass('BACProjectile', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'skill_id',
    'use_cmn_bsa',
    'bsa_id',
    'bone_to_spawn_from',
    'spawn_source',
    'position_x',
    'position_y',
    'position_z',
    'rotation_x',
    'rotation_y',
    'rotation_z',
    'skill_bsa_flags',
    'projectile_flags',
    'projectile_health',
    'unique_id',
    'u_38',
    'u_3c'
])


# Type 9
class Projectile(BaseType):
    type = 9
    bac_record = BACProjectile
    byte_order = 'HHHHHHIHHffffffHHIIII'
    size = 64
    dependencies = {
        ('skill_id', None): {},
        ('bsa_id', 'use_cmn_bsa'): {0x0: 'Yes'}
    }

    description_type = "skill_bsa_flags"
    description = {
        0x0: "CMN",
        0x3: "Awoken",
        0x5: "Super",
        0x6: "Ultimate",
        0x7: "Evasive",
        0x8: "Blast"
    }

    def __init__(self, index):
        super().__init__(index)

    def read(self, f, endian, _):
        self.data = self.bac_record(*struct.unpack(endian + self.byte_order, f.read(self.size)))
        self.data.rotation_x = math.degrees(self.data.rotation_x)
        self.data.rotation_y = math.degrees(self.data.rotation_y)
        self.data.rotation_z = math.degrees(self.data.rotation_z)

    def write(self, f, endian):
        backup_x = self.data.rotation_x
        backup_y = self.data.rotation_y
        backup_z = self.data.rotation_z

        self.data.rotation_x = math.radians(self.data.rotation_x)
        self.data.rotation_y = math.radians(self.data.rotation_y)
        self.data.rotation_z = math.radians(self.data.rotation_z)
        f.write(struct.pack(endian + self.byte_order, *self.data))

        self.data.rotation_x = backup_x
        self.data.rotation_y = backup_y
        self.data.rotation_z = backup_z
