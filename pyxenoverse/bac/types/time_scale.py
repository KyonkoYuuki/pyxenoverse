from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACTimeScale = recordclass('BACTimeScale', ['start_time', 'duration', 'u_04', 'character_type', 'time_scale'])


# Type 4
class TimeScale(BaseType):
    type = 4
    bac_record = BACTimeScale
    byte_order = 'HHHHf'
    size = 12

    def __init__(self, index):
        super().__init__(index)
