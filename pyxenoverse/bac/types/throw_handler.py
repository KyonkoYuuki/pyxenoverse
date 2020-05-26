from recordclass import recordclass
import struct

from pyxenoverse.bac.types import BaseType

BACThrowHandler = recordclass('BACThrowHandler', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'throw_flags',
    'u_0a',
    'bone_user_connects_to_victim_from',
    'bone_victim_connects_to_user_from',
    'bac_entry',
    'u_12',
    'victim_displacement_x',
    'victim_displacement_y',
    'victim_displacement_z'
])


# Type 17
class ThrowHandler(BaseType):
    type = 17
    bac_record = BACThrowHandler
    byte_order = 'HHHHHHHHHH'
    size = 20
    displacement_size = 12

    def __init__(self, index):
        super().__init__(index)

    def get_size(self, type17_small):
        size = self.size
        if not type17_small:
            size += self.displacement_size
        return size

    def read(self, f, endian, type17_small):
        self.data = self.bac_record(*struct.unpack(endian + self.byte_order, f.read(self.size)), 0.0, 0.0, 0.0)
        if not type17_small:
            self.data[10:] = struct.unpack(endian + 'fff', f.read(self.displacement_size))

    def write(self, f, endian):
        f.write(struct.pack(endian + self.byte_order + 'fff', *self.data))


