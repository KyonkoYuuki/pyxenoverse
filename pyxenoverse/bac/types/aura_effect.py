from recordclass import recordclass

from pyxenoverse.bac.types import BaseType


BACAuraEffect = recordclass('BACAuraEffect', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'type',
    'on_off_switch',
    'u_0c'
])


# Type 19
class AuraEffect(BaseType):
    type = 19
    bac_record = BACAuraEffect
    byte_order = 'HHHHHHI'
    size = 16

    def __init__(self, index):
        super().__init__(index)
