from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACBcmCallback = recordclass('BACBcmCallback', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'bcm_link_flags',
    'u_0a'
])


# Type 7
class BcmCallback(BaseType):
    type = 7
    bac_record = BACBcmCallback
    byte_order = 'HHHHHH'
    size = 12

    def __init__(self, index):
        super().__init__(index)
