from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACChargeAttackParameters = recordclass('BACChargeAttackParameters', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'total_charge_time',
    'u_0e'
])


# Type 6
class ChargeAttackParameters(BaseType):
    type = 25
    bac_record = BACChargeAttackParameters
    byte_order = 'HHHHIHH'
    size = 16

    def __init__(self, index):
        super().__init__(index)
