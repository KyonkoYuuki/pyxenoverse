import struct

from pyxenoverse import BaseRecord


class BaseType(BaseRecord):
    def __init__(self):
        super().__init__()
        self.data = self.bac_record(*([0] * len(self.bac_record.__attrs__)))

    def read(self, f, endian):
        self.data = self.bac_record(*struct.unpack(endian + self.byte_order, f.read(self.size)))

    def write(self, f, endian):
        f.write(struct.pack(endian + self.byte_order, *self.data))
