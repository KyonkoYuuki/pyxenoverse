from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAMovement = recordclass('BSAMovement', [
    'motion_flags',
    'speed_z',
    'speed_x',
    'speed_y',
    'f_16',
    'acceleration_z',
    'acceleration_x',
    'acceleration_y',
    'falloff_strength',
    'spread_x',
    'spread_y',
    'spread_z',
])


# Type 1
class Movement(BaseType):
    type = 1
    bsa_record = BSAMovement
    byte_order = 'Ifffffffffff'
    size = 48

    def __init__(self, index):
        super().__init__(index)
