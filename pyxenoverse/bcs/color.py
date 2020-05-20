import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name

BCSColor = recordclass('BCSColor', [
    'f_00',
    'f_04',
    'f_08',
    'f_0c',
    'f_10',
    'f_14',
    'f_18',
    'f_1c',
    'f_20',
    'f_24',
    'f_28',
    'f_2c',
    'f_30',
    'f_34',
    'f_38',
    'f_3c',
    'f_40',
    'f_44',
    'f_48',
    'f_4c',

])
BCS_COLOR_SIZE = 80
BCS_COLOR_BYTE_ORDER = 'ffffffffffffffffffff'


class Color(BaseRecord):
    def __init__(self):
        super().__init__()
        self.data = BCSColor(*([0] * len(BCSColor.__fields__)))

    def read(self, f, endian):
        self.data = BCSColor(*struct.unpack(endian + BCS_COLOR_BYTE_ORDER, f.read(BCS_COLOR_SIZE)))
        # print(self.data)

    def write(self, f, endian):
        f.write(struct.pack(endian + BCS_COLOR_BYTE_ORDER, *self.data))
