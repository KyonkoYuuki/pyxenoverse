from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACTargetingAssistance = recordclass('BACTargetingAssistance', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'rotation_axis',
    'u_0a'
])


# Type 12
class TargetingAssistance(BaseType):
    type = 12
    bac_record = BACTargetingAssistance
    byte_order = 'HHHHHH'
    size = 12

    def __init__(self, index):
        super().__init__(index)
