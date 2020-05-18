from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACCamera = recordclass('BACCamera', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'ean_type',
    'bone_to_focus_on',
    'ean_index',
    'frame_start',
    'u_10',
    'u_12',
    'z_position',
    'x_z_disposition',
    'y_z_disposition',
    'x_rotation',
    'y_rotation',
    'x_position',
    'y_position',
    'zoom',
    'z_rotation',
    'u_38',
    'u_3c',
    'u_40',
    'u_44',
    'u_48',
    'camera_flags'
])


# Type 10
class Camera(BaseType):
    type = 10
    dependencies = {
        ('ean_index', 'ean_type'): {0x4: 'Character', 0x5: 'Skill'}
    }
    bac_record = BACCamera
    byte_order = 'HHHHHHHHHHfffffffffIIIIHH'
    size = 76

    def __init__(self, index):
        super().__init__(index)
