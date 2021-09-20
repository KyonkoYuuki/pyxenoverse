from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACEyeMovement = recordclass('BACEyeMovement', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'u_0c',
    'direction_type',
    'rotation',
    'eye_duration',
    'u_16',
    'f_18',
    'f_1c'
])


# Type 21
class EyeMovement(BaseType):
    type = 21
    bac_record = BACEyeMovement
    byte_order = 'HHHHIHHIHHff'
    size = 32

    direction_type_dict = {0x0 : "Left",
                          0x1 : "Up",
                          0x2 : "Right",
                          0x3 : "Left",
                          0x4 : "None",
                          0x5 : "Right",
                          0x6 : "Left-Down",
                          0x7 : "Down",
                          0x8 : "Ki Right-Down"}



    def __init__(self, index):
        super().__init__(index)
