from recordclass import recordclass

from pyxenoverse.bac.types import BaseType


BACAuraEffect = recordclass('BACAuraEffect', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'aura_type',
    'on_off_switch',
    'u_0c'
])


# Type 19
class AuraEffect(BaseType):
    type = 19
    bac_record = BACAuraEffect
    byte_order = 'HHHHHHI'
    size = 16

    aura_type_dict = {0x0 : "Boost start",
                      0x1 : "Boost loop",
                      0x2 : "Boost end",
                      0x3 : "Ki charge loop",
                      0x4 : "Ki charge end",
                      0x5 : "Transform aura loop",
                      0x6 : "Transform aura end"}




    def __init__(self, index):
        super().__init__(index)
