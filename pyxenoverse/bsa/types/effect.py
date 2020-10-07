from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAEffect = recordclass('BSAEffect', [
    'eepk_type',
    'skill_id',
    'effect',
    'i_06',
    'effect_switch',
    'i_10',
    'position_x',
    'position_y',
    'position_z'
])


# Type 6
class Effect(BaseType):
    type = 6
    bac_record = BSAEffect
    byte_order = 'HHHHHHfff'
    size = 24

    def __init__(self, index):
        super().__init__(index)
