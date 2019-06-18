from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACAnimation = recordclass('BACAnimation', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'ean_type',
    'ean_index',
    'u_0c',
    'u_0e',
    'frame_start',
    'frame_end',
    'frame_loop_start',
    'u_16',
    'speed',
    'transitory_animation_connection_type',
    'transitory_animation_compression'
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

    def __init__(self, index):
        super().__init__(index)

