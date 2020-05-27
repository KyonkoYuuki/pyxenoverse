from recordclass import recordclass

from pyxenoverse.bac.types import BaseType

BACTransparencyEffect = recordclass('BACTransparencyEffect', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'transparency_flags',
    'transparency_flags2',
    'dilution',
    'u_0e',
    'u_10',
    'red',
    'green',
    'blue',
    'f_20',
    'f_24',
    'f_28',
    'f_2c',
    'f_30',
    'f_34',
    'f_38',
    'f_3c'
])


# Type 23
class TransparencyEffect(BaseType):
    type = 23
    bac_record = BACTransparencyEffect
    byte_order = 'HHHHHHHHIfffffffffff'
    size = 64

    def __init__(self, index):
        super().__init__(index)
        self.color = [0, 0, 0]

    def read(self, f, endian, _):
        super().read(f, endian, _)
        self.red = int(self.red * 255.0)
        self.green = int(self.green * 255.0)
        self.blue = int(self.blue * 255.0)
        self.color = [self.red, self.green, self.blue]

    def write(self, f, endian):
        self.red, self.green, self.blue = self.color
        self.red /= 255.0
        self.green /= 255.0
        self.blue /= 255.0
        super().write(f, endian)
