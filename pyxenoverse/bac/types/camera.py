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

    'duration_all',
    'z_position',
    'x_z_disposition',
    'y_z_disposition',

    'y_rotation',
    'x_rotation',
    'x_position',
    'y_position',

    'zoom',
    'z_rotation',
    'z_position_duration',
    'displacement_xz_duration',

    'displacement_yz_duration',
    'y_rotation_duration',
    'x_rotation_duration',
    'x_position_duration',

    'y_position_duration',
    'zoom_duration',
    'z_rotation_duration',
    'camera_flags'
])


# Type 10
class Camera(BaseType):
    type = 10
    dependencies = {
        ('ean_index', 'ean_type'): {0x4: 'Character', 0x5: 'Skill'}
    }

    description_type = "ean_type"
    description = {
        0x0: "Rumble",
        0x1: "Heavy Rumble",
        0x2: "Extreme Rumble",
        0x3: "CMN.cam.ean",
        0x4: "Character",
        0x5: "Skill",
        0x6: "Zoom",
        0x7: "Static",
        0x8: "Victim",
        0x9: "Unknown (0x9)",
        0xa: "Zoom/speed lines",
        0xb: "Battle Camera",
        0xc: "Cinematic (0xc)",
        0xd: "Look at Target",
        0xe: "Small Rumble",
        0xf: "Ultra Rumble",
        0x11: "Zoom into player",
        0x14: "Unknown (0x14)",
        0x13: "Unknown (0x13)",
        0x16: "Unknown (0x16)",
        0x19: "Activate Extended Camera",
        0x1a: "Unknown (0x1a)",
        0x20: "Deactivate Extended Camera"
    }

    bac_record = BACCamera
    byte_order = 'HHHHH HHHH Hfff ffff ffHH HHHH HHHH'
    size = 76

    def __init__(self, index):
        super().__init__(index)
