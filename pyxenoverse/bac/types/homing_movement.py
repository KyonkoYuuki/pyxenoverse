from recordclass import recordclass
import struct

from pyxenoverse.bac.types import BaseType

BACHomingMovement = recordclass('BACHomingMovement', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'type',
    'horizontal_homing_arc_direction',
    'speed_modifier',
    'u_10',
    'horizontal_direction_modifier',
    'vertical_direction_modifier',
    'z_direction_modifier',
    'u_20',
    'u_24',
    'u_28',
    'u_2c'
])


# Type 20
class HomingMovement(BaseType):
    type = 20
    bac_record = BACHomingMovement
    byte_order = 'HHHHHHIIfffIIII'
    size = 48

    def __init__(self, index):
        super().__init__(index)

    def read(self, f, endian, _):
        address = f.tell()
        super().read(f, endian, _)

        # Read the speed modifier as a float
        if self.horizontal_homing_arc_direction == 0x7:
            f.seek(address + 12)
            self.speed_modifier = struct.unpack(endian + "f", f.read(4))[0]

    def write(self, f, endian):
        address = f.tell()
        speed_modifier_float = float(self.speed_modifier)

        # Write speed modifier as an int first
        self.speed_modifier = int(self.speed_modifier)
        super().write(f, endian)

        # Write it as a float
        if self.horizontal_homing_arc_direction == 0x7:
            self.speed_modifier = speed_modifier_float
            f.seek(address + 12)
            f.write(struct.pack(endian + "f", self.speed_modifier))
