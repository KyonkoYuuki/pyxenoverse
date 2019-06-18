from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACDualSkillData = recordclass('BACDualSkillData', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'u_0a',
    'u_0c',
    'u_0e',
    'u_10',
    'f_14',
    'f_18',
    'f_1c',
    'u_20',
    'u_22',
    'u_24',
    'f_28',
    'f_2c',
    'f_30',
    'u_34',
    'u_36'
])


# Type 24
class DualSkillData(BaseType):
    type = 24
    bac_record = BACDualSkillData
    byte_order = 'HHHHHHHHIfffHHIfffHH'
    size = 56

    def __init__(self, index):
        super().__init__(index)
