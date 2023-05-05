from recordclass import recordclass

from pyxenoverse.bsa.types import BaseType

BSAScreenEffect = recordclass('BSAScreenEffect', [
    'bpe_effect_id',
    'i_02',
    'i_04',
    'i_08',
    'i_12',
    'i_16',
    'i_20'
])


# ScreenEffect
class ScreenEffect(BaseType):
    type = 8
    bsa_record = BSAScreenEffect
    byte_order = 'HHIIIII'
    size = 24

    description_type = "bpe_effect_id"
    description = {
        0: 'Brightens up the screen',
        1: 'White Screen',
        2: 'Brightens up the screen',
        3: 'Quick White Flash',
        4: 'Brightness Wavering',
        5: 'Red Tint',
        6: 'Fast Brightness Wavering',
        10: 'Small Motion Blur',
        11: 'Strong Motion Blur',
        12: 'Quick Motion Blur,',
        13: 'Very Small Motion Blur',
        14: 'Light Blue Filter',
        15: 'Quick Motion Blur',
        16: 'Quick Motion Blur',
        17: 'Magenta Filter',
        18: 'Two Different Motion Blurs',
        20: 'Ripple Blur',
        21: 'Ripple Blur',
        22: 'Ripple Blur',
        23: 'Ripple Blur',
        24: 'Gravely Blur',
        25: 'Gravely Blur',
        26: 'Ripple Blur ',
        27: 'Ripple Blur',
        30: 'Solar Flare Screen Effect (Opponent Blind)',
        31: 'blackening around the screen',
        32: 'blackening around the screen',
        33: 'Faint Black Circle',
        34: 'A pair of faint Black Circles',
        35: 'faint Black Circle',
        36: 'Solar Flare Screen Effect (User Activate)',
        37: 'Screen turns completely black',
        40: 'Small Transparent Ring expanding',
        41: 'Transparent Ring',
        42: 'Transparent Ring',
        43: 'Big Transparent Ring',
        44: 'Big Transparent Ring',
        45: 'Big Transparent Ring',
        46: 'Transparent Ring',
        50: 'Brightening of the Screen',
        51: 'Brightening of the Screen',
        52: 'Big Transparent Ring',
        53: 'Blue Tint',
        54: 'blackening around the screen',
        55: 'Screen slightly darkens and desaturates',
        56: 'Screen slightly darkens and desaturates',
        57: 'Screen slightly darkens and desaturates',
        60: 'Screen flashes a faint white',
        61: 'Screen slightly darkens and desaturates',
        63: 'Screen slightly darkens and desaturates',
        64: 'Screen flashes a faint pink for a second',
        65: 'Light Blue Filter Fades in and out',
        66: 'Black Spheres',
        70: 'Standard Black Filter used during Skill Activations'
    }

    def __init__(self, index):
        super().__init__(index)
