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

    description_type = "rotation_axis"
    description = {
        0x0: "X",
        0x1: "Y",
        0x2: "Z",
        0x3: "Unknown (0x3)",
        0x4: "Unknown (0x4)",
        0x8: "Unknown (0x8)",
        0xc: "Unknown (0xc)",
    }

    def __init__(self, index):
        super().__init__(index)
