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

    'y_rotation',
    'x_rotation',
    'x_position',
    'y_position',

    'zoom',
    'z_rotation',
    'u_36',
    'u_38',

    'u_3a',
    'u_3c',
    'u_3e',
    'u_40',

    'u_42',
    'zoom_duration',
    'u_48',
    'camera_flags'
])


# Type 10
class Camera(BaseType):
    type = 10
    dependencies = {
        ('ean_index', 'ean_type'): {0x4: 'Character', 0x5: 'Skill'}
    }

    ean_type_dict = { 0x0 : "Basic Lock",
                      0x1 : "Heavy Rumble",
                      0x2 : "Extreme Rumble",
                      0x3 : "CMN.cam.ean",
                      0x4 : "Character",
                      0x5 : "Skill",
                      0x6 : "Zoom",
                      0x7 : "Static",
                      0x8 : "Victim",
                      0xa : "Zoom/speed lines",
                      0xb : "Cinematic (0xb)",
                      0xc : "Cinematic (0xc)",
                      0xe : "Heavy Rumble",
                      0xf : "Extreme Rumble",
                      0x11 : "Zoom into player",
                      0x19 : "Activate Extended Camera",
                      0x20 : "Deactivate Extended Camera"}



    bac_record = BACCamera
    byte_order = 'HHHHH HHHH Hfff ffff ffHH HHHH HHHH'
    size = 76

    def __init__(self, index):
        super().__init__(index)
