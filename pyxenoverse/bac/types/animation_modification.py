from recordclass import recordclass

from pyxenoverse.bac.types import BaseType
BACAnimationModification = recordclass('BACAnimationModification', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'modification',
    'u_0a'
])


# Type 14
class AnimationModification(BaseType):
    type = 14
    bac_record = BACAnimationModification
    byte_order = 'HHHHHH'
    size = 12

    def __init__(self, index):
        super().__init__(index)
