from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACMotionAdjust = recordclass('BACMotionAdjust', ['start_time', 'duration', 'u_04', 'character_type', 'time_scale'])


# Type 4
class MotionAdjust(BaseType):
    type = 4
    bac_record = BACMotionAdjust
    byte_order = 'HHHHf'
    size = 12

    def __init__(self, index):
        super().__init__(index)
