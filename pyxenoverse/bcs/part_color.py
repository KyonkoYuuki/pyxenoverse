import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name
from pyxenoverse.bcs.color import Color

BCSPartColor = recordclass('BCSPartColor', [
    'name_offset',
    'u_04',
    'u_08',
    'num',
    'colors_offset'
])
BCS_PART_COLOR_SIZE = 16
BCS_PART_COLOR_BYTE_ORDER = 'IIHHI'


class PartColor(BaseRecord):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.colors = []
        self.data = BCSPartColor(*([0] * len(BCSPartColor.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSPartColor(*struct.unpack(endian + BCS_PART_COLOR_BYTE_ORDER, f.read(BCS_PART_COLOR_SIZE)))
        # print(self.data)
        if self.name_offset:
            self.name = read_name(f, address + self.name_offset)
            # print(f'name: {self.name}')
        self.colors.clear()
        f.seek(address + self.colors_offset)
        for i in range(self.num):
            color = Color()
            color.read(f, endian)
            self.colors.append(color)

    def write(self, f, names, colors, endian):
        address = f.tell()
        self.num = len(self.colors)
        self.name_offset = 0
        self.colors_offset = 0
        f.write(struct.pack(endian + BCS_PART_COLOR_BYTE_ORDER, *self.data))

        # Add Name
        if self.name:
            names.append((address, 0, self.name))

        # Add colors
        if self.colors:
            colors.append((address, 0xc, self.colors))

        return f.tell()
