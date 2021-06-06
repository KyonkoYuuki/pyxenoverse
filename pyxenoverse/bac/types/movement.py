from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACAccelerationMovement = recordclass('BACAccelerationMovement', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'movement_flags',
    'u_0a',
    'x_axis_movement',
    'y_axis_movement',
    'z_axis_movement',
    'x_axis_drag',
    'y_axis_drag',
    'z_axis_drag'
])


# Type 2
class Movement(BaseType):
    type = 2
    bac_record = BACAccelerationMovement
    byte_order = 'HHHHHHffffff'
    size = 36

    def __init__(self, index):
        super().__init__(index)
