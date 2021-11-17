from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACAnimation = recordclass('BACAnimation', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'ean_type',
    'ean_index',
    'animation_flags',
    'play_face_animation_from_skill',
    'frame_start',
    'frame_end',
    'frame_loop_start',
    'u_16',
    'speed',
    'animation_transition_start_frame',
    'animation_transition_frame_step'
])


# Type 0
class Animation(BaseType):
    type = 0
    bac_record = BACAnimation
    byte_order = 'HHHHHHHHHHHHfff'
    size = 36

    dependencies = {
        ('ean_index', 'ean_type'): {0x5: 'Character', 0xFFFE: 'Skill'}
    }
    description_type = "ean_type"
    description = {
        0x0: "CMN.ean",
        0x1: "Unknown (0x1)",
        0x2: "Unknown (0x2)",
        0x5: "Char. EAN",
        0x6: "Unknown (0x6)",
        0x9: "CMN.tal.ean (tail)",
        0xa: "Char. fce.ean (mouth)",
        0xb: "Char. fce.ean (eye)",
        0x28: "Unknown (0x28)",
        0x29: "Unknown (0x29)",
        0x2a: "Unknown (0x2a)",
        0x2b: "Unknown (0x2b)",
        0xfffe: "Skill Ean"
    }

    def __init__(self, index):
        super().__init__(index)
