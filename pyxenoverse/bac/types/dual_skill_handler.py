from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACDualSkillHandler = recordclass('BACDualSkillHandler', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'dual_skill_handler_flags',
    'u_0a',
    'u_0c',
    'u_0e',
    'u_10',
    'position_initiator_x',
    'position_initiator_y',
    'position_initiator_z',
    'u_20',
    'u_22',
    'u_24',
    'position_partner_x',
    'position_partner_y',
    'position_partner_z',
    'u_34',
    'u_36'
])


# Type 24
class DualSkillHandler(BaseType):
    type = 24
    bac_record = BACDualSkillHandler
    byte_order = 'HHHHHHHHIfffHHIfffHH'
    size = 56

    def __init__(self, index):
        super().__init__(index)
