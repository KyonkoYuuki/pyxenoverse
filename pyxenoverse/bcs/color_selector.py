import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord

from xml.etree.ElementTree import SubElement, Comment

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

    def generate_xml(self, root, part_colors=None):
        color_selector = SubElement(root, "ColorSelector")
        name = ''

        # Part Colors
        if part_colors:
            name = part_colors[self.part_colors].name
            color_selector.append(Comment(name))
        SubElement(color_selector, "PART_COLORS", value=str(self.part_colors))

        # Color
        if part_colors:
            color = part_colors[self.part_colors].colors[self.color]
            if name == 'eye_':
                rgba = color.color4
            else:
                rgba = color.color1

            hex_color = f'#{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}'
            color_selector.append(Comment(f"Color preview: {hex_color}"))
        SubElement(color_selector, "COLOR", value=str(self.color))
