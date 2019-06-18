from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACTransformControl = recordclass('BACTransformControl', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'type',
    'u_0a',
    'f_0c',
    'f_10',
    'f_14',
    'u_18',
    'u_1c'
])


# Type 15
class TransformControl(BaseType):
    type = 15
    bac_record = BACTransformControl
    byte_order = 'HHHHHHfffII'
    size = 32

    def __init__(self, index):
        super().__init__(index)
