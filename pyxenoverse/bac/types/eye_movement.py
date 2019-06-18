from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACEyeMovement = recordclass('BACEyeMovement', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'u_0c',
    'direction',
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

    def __init__(self, index):
        super().__init__(index)
