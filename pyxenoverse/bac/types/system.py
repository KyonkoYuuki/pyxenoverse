from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACSystem = recordclass('BACSystem', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'function_type',
    'u_0a',
    'f_0c',
    'f_10',
    'f_14',
    'f_18',
    'f_1c'
])


# Type 15
class System(BaseType):
    type = 15
    bac_record = BACSystem
    byte_order = 'HHHHHHfffff'
    size = 32

    description_type = "function_type"
    description = {
        0x0: 'Loop',
        0x2: 'Damage',
        0x4: 'Give/take Ki',
        0x6: 'Invisibility',
        0x7: 'Rotate animation',
        0xb: 'Override throw duration',
        0xc: 'Darken Screen',
        0xd: 'Activate transformation',
        0xe: 'Deactivate transformation',
        0xf: 'Damage user once',
        0x10: 'Detonate Projectiles',
        0x11: 'Swap bodies',
        0x12: 'Target/untarget',
        0x13: 'Set BCS Part',
        0x14: 'Set BCS Part',
        0x15: 'Remove user',
        0x16: 'Give/take stamina',
        0x1b: 'Limited transformation',
        0x1d: 'Go to entry',
        0x1f: 'Reset Camera',
        0x20: 'Disable movement/skill',
        0x22: 'Loop (Hold Down)',
        0x23: 'Floating rocks',
        0x24: 'Knock away rocks',
        0x25: 'Go to entry at end',
        0x26: 'Change projectile',
        0x28: 'Invisible opponents',
        0x29: 'Untargetable player',
        0x2a: 'BCS Bonescale',
        0x2d: 'No-clip',
        0x2e: 'Big collision box',
        0x30: 'Black void',
        0x31: 'Regen health',
        0x3c: 'Stun',
        0x3f: 'Limit burst',
        0x43: 'Auto-dodge',
        0x44: 'Damage x10',
        0x4c: 'Activate Buff',
        0x4d: 'Count-Specific Loop (Hold Down)',
        0x4e: 'Skill Upgrade'
    }

    def __init__(self, index):
        super().__init__(index)
