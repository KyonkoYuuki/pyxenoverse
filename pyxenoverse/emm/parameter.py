import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord


EMMParameter = recordclass('EMMParameter', ['name', 'type', 'value'])
EMM_PARAMETER_SIZE = 40
EMM_PARAMETER_BYTE_ORDER = '32sIf'


class Parameter(BaseRecord):
    def __init__(self):
        super().__init__()
        self.data = EMMParameter('', 0, 0)

    def read(self, f, endian):
        self.data = EMMParameter(*struct.unpack(endian + EMM_PARAMETER_BYTE_ORDER, f.read(EMM_PARAMETER_SIZE)))
        self.name = self.name.decode().strip('\0')
        print(self)

    def write(self, f, endian):
        self.name = self.name.ljust(32, '\0').encode()
        f.write(struct.pack(endian + EMM_PARAMETER_BYTE_ORDER, *self.data))
