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

FUNCTION_MAPPINGS = {
    0x0: ('Loop', None, None, None, None, None),
    0x2: ('Damage', 'Damage', None, None, None, None),
    0x4: ('Give/take Ki', 'Ki', None, None, None, None),
    0x6: ('Invisibility', None, None, None, None, None),
    0x7: ('Rotate animation', 'Y-axis Degrees', None, None, None, None),
    0x8: ('Viberate Controller', None, None, None, None, None),
    0x9: ('Viberate Controller', None, None, None, None, None),
    0xb: ('Override throw duration', 'Duration', None, None, None, None),
    0xc: ('Darken Screen', None, None, None, None, None),
    0xd: ('Activate transformation', None, None, None, None, None),
    0xe: ('Deactivate transformation', None, None, None, None, None),
    0xf: ('Damage user once', None, None, None, None, None),
    0x10: ('Detonate Projectiles', 'BAC Condition', None, None, None, None),
    0x11: ('Swap bodies', None, None, None, None, None),
    0x12: ('Target/untarget', None, None, None, None, None),
    0x13: ('Set BCS Part (Temporary)', 'Partset Id', None, None, None, None),
    0x14: ('Set BCS Part (Permanent)', 'Partset Id', None, None, None, None),
    0x15: ('Remove user', None, None, None, None, None),
    0x16: ('Give/take stamina', 'Stamina', None, None, None, None),
    0x1b: ('Limited transformation', None, None, None, None, None),
    0x1d: ('Go to entry', 'BAC Entry', None, None, None, None),
    0x1f: ('Reset Camera', None, None, None, None, None),
    0x2f: ('Display Time Skip Behavior', None, None, None, None, None),
    0x20: ('Disable movement/skill', None, None, None, None, None),
    0x22: ('Loop (Hold Down)', None, None, None, None, None),
    0x23: ('Floating rocks', None, None, None, None, None),
    0x24: ('Knock away rocks', None, None, None, None, None),
    0x25: ('Go to entry at end', 'BAC Entry ID', 'Skill Type', 'Skill Id', None, None),
    0x26: ('Change projectile', 'BSA Condition', 'Skill Type', 'Skill Id', 'F_18', 'F_1C'),
    0x28: ('Invisible opponents', None, None, None, None, None),
    0x29: ('Untargetable player', None, None, None, None, None),
    0x2a: ('BCS Bonescale', 'Bonescale Id', None, None, None, None),
    0x2d: ('No-clip', 'Unknown', None, None, None, None),
    0x2e: ('Big collision box', 'Unknown', None, None, None, None),
    0x30: ('Black void', None, None, None, None, None),
    0x31: ('Regen health', 'Health', None, None, None, None),
    0x39: ('Split Camera for Dual Skills', 'Unknown', None, None, None, None),
    0x3c: ('Stun', 'Stun Duration', None, None, None, None),
    0x3f: ('Limit burst', None, None, None, None, None),
    0x43: ('Auto-dodge', 'Stamina cost', None, None, None, None),
    0x44: ('Damage x10', 'Damage', None, None, None, None),
    0x4a: ('Skill Cooldown', 'Cooldown duration', None, None, None, None),
    0x4f: ('Rotate b_C_Base', 'Rotation Angle?', None, None, None, None),
    0x4c: ('Activate Buff', 'Super Soul ID', None, None, None, None),
    0x4d: ('Count-Specific Loop (Hold Down)', 'Loop Step', "Skill ID", "Skill Type", "Loop Count", None),
    0x4e: ('Skill Upgrade', 'Skill Id', 'Skill Type', 'Upgrade Cmd', 'F_18', 'F_1C'),
    0x50: ('Allow Evasive Usage', 'Unknown', 'Start Frame', 'Unknown', None, None),
    0x58: ('Guard Against Projectile', 'Power Level?', None, None, None, None),
    0x59: ('Untarget Opponent', None, None, None, None, None),

    0x5f: ('Auto-dodge', 'Stamina cost', 'HP Condition %', None, None, None),


}


# Type 15
class System(BaseType):
    type = 15
    bac_record = BACSystem
    byte_order = 'HHHHHHfffff'
    size = 32

    description_type = "function_type"
    description = {k: v[0] for k, v in FUNCTION_MAPPINGS.items()}

    def __init__(self, index):
        super().__init__(index)
