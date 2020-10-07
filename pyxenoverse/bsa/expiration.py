import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord

BSAExpiration = recordclass('BSAExpiration', [
    'i_00',
    'i_02',
    'i_04',
    'i_06',
])

BSA_EXPIRATION_SIZE = 8

BSA_EXPIRATION_BYTE_ORDER = 'HHHH'


class Expiration(BaseRecord):
    def __init__(self):
        super().__init__()
        self.data = BSAExpiration(*([0] * len(BSAExpiration.__fields__)))

    def read(self, f, endian):
        self.data = BSAExpiration(*struct.unpack(endian + BSA_EXPIRATION_BYTE_ORDER, f.read(BSA_EXPIRATION_SIZE)))
        # print(self.data)

    def write(self, f, endian):
        f.write(struct.pack(endian + BSA_EXPIRATION_BYTE_ORDER, *self.data))

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BSAExpiration(*other.data)
        return True
