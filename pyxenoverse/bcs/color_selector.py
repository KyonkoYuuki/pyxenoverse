import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord

BCSColorSelector = recordclass('BCSColorSelector', [
    'part_colors',
    'color'
])
BCS_COLOR_SELECTOR_SIZE = 4
BCS_COLOR_SELECTOR_BYTE_ORDER = 'HH'


class ColorSelector(BaseRecord):
    def __init__(self):
        super().__init__()
        self.data = BCSColorSelector(*([0] * len(BCSColorSelector.__fields__)))

    def read(self, f, endian):
        self.data = BCSColorSelector(*struct.unpack(endian + BCS_COLOR_SELECTOR_BYTE_ORDER, f.read(BCS_COLOR_SELECTOR_SIZE)))
        # print(self.data)

    def write(self, f, endian):
        f.write(struct.pack(endian + BCS_COLOR_SELECTOR_BYTE_ORDER, *self.data))

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSColorSelector(*other.data)
        return True
