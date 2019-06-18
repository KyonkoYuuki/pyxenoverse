from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACHomingMovement = recordclass('BACHomingMovement', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'type',
    'horizontal_homing_arc_direction',
    'speed_modifier',
    'u_10',
    'horizontal_direction_modifier',
    'vertical_direction_modifier',
    'z_direction_modifier',
    'u_20',
    'u_24',
    'u_28',
    'u_2c'
])


# Type 20
class HomingMovement(BaseType):
    type = 20
    bac_record = BACHomingMovement
    byte_order = 'HHHHHHIIfffIIII'
    size = 48

    def __init__(self, index):
        super().__init__(index)
