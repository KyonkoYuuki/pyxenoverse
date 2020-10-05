from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACEffectPropertyControl = recordclass('BACEffectPropertyControl', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'skill_id',
    'u_0a',
    'u_0c',
    'u_0e',
    'skill_type',
    'effect_id',
    'effect_duration',
    'flags'
])


# Type 27
class EffectPropertyControl(BaseType):
    type = 27
    bac_record = BACEffectPropertyControl
    byte_order = 'HHHHHHHHHHHH'
    size = 24

    def __init__(self, index):
        super().__init__(index)
