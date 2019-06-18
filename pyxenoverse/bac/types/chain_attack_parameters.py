from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACChainAttackParameters = recordclass('BACChainAttackParameters', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'total_chain_time',
    'u_0e'
])


# Type 6
class ChainAttackParameters(BaseType):
    type = 6
    bac_record = BACChainAttackParameters
    byte_order = 'HHHHIHH'
    size = 16

    def __init__(self, index):
        super().__init__(index)
