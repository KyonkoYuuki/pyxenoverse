from recordclass import recordclass
import re

from pyxenoverse.bac.types import BaseType

BACType22 = recordclass('BACType22', [
    'start_time',
    'duration',
    'u_04',
    'character_type',
    'u_08',
    'f_0c',
    'name'
])


# Type 22
class Type22(BaseType):
    type = 22
    bac_record = BACType22
    byte_order = 'HHHHIf32s'
    size = 48

    def __init__(self, index):
        super().__init__(index)

    def read(self, f, endian, _):
        super().read(f, endian, _)
        self.name = re.sub(r'[^\x20-\x7f]', '', self.name.decode())

    def write(self, f, endian):
        if isinstance(self.name, str):
            self.name = self.name.encode()
        super().write(f, endian)
