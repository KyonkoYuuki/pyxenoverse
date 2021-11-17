from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACEyeMovement = recordclass('BACEyeMovement', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'previous_eye_direction',
    'next_direction',
    'frames_until_eyes_reach_rotation',
    'eye_movement_duration',
    'u_16',
    'left_eye_rotation_percent',
    'right_eye_rotation_percent'
])


# Type 21
class EyeMovement(BaseType):
    type = 21
    bac_record = BACEyeMovement
    byte_order = 'HHHHIHHIHHff'
    size = 32

    description_type = "next_direction"
    description = {
        0x0: "Left",
        0x1: "Up",
        0x2: "Right",
        0x3: "Left-Up",
        0x4: "None",
        0x5: "Right-Up",
        0x6: "Left-Down",
        0x7: "Down",
        0x8: "Right-Down"
    }

    def __init__(self, index):
        super().__init__(index)
