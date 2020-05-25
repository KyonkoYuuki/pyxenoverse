import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bcs.part import Part

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom

BCSPartSet = recordclass('BCSPartSet', [
    'u_00',
    'u_04',
    'u_08',
    'u_0c',
    'u_10',
    'num_parts',
    'table_start',
    'u_1c',
    'face_base_offset',
    'face_forehead_offset',
    'eye_base_offset',
    'nose_offset',
    'ear_offset',
    'hair_offset',
    'bust_offset',
    'pants_offset',
    'wrists_offset',
    'boots_offset'
])
BCS_PART_SET_SIZE = 72
BCS_PART_SET_BYTE_ORDER = 'IIIIIIIIIIIIIIIIII'

BCS_PART_LIST = [
    "face_base",
    "face_forehead",
    "eye_base",
    "nose",
    "ear",
    "hair",
    "bust",
    "pants",
    "wrists",
    "boots"
]


class PartSet(BaseRecord):
    def __init__(self):
        super().__init__()
        self.parts = {}
        self.data = BCSPartSet(*([0] * len(BCSPartSet.__fields__)))

    def read(self, f, endian):
        address = f.tell()
        # print(address)
        self.data = BCSPartSet(*struct.unpack(endian + BCS_PART_SET_BYTE_ORDER, f.read(BCS_PART_SET_SIZE)))
        # print(self.data)

        self.num_parts = 10  # never changes
        self.table_start = 0x20  # never changes
        self.parts.clear()
        for part_name in BCS_PART_LIST:
            offset = self[part_name + "_offset"]
            if not offset:
                continue
            part = Part()
            f.seek(address + offset)
            # print(part_name)
            part.read(f, endian)
            self.parts[part_name] = part

    def write(self, f, names, endian):
        start_address = f.tell()
        f.seek(start_address + BCS_PART_SET_SIZE)
        for part_name in BCS_PART_LIST:
            if part_name not in self.parts:
                self[part_name + "_offset"] = 0
                continue
            self[part_name + "_offset"] = f.tell() - start_address
            self.parts[part_name].write(f, names, endian)

        end_address = f.tell()
        f.seek(start_address)
        f.write(struct.pack(endian + BCS_PART_SET_BYTE_ORDER, *self.data))
        return end_address

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSPartSet(*other.data)
        self.parts = other.parts.copy()
        return True

    def generate_xml(self, part_colors=None):
        root = Element("PartSet")
        for idx, part_name in enumerate(BCS_PART_LIST):
            part_element = SubElement(root, "Part", idx=str(idx))
            part_element.append(Comment(part_name.capitalize()))
            if part_name not in self.parts:
                part_element.append(Comment("This entry is empty."))
            else:
                part = self.parts[part_name]
                part.generate_xml(part_element, part_colors)
        print(tostring(root))
        dom = xml.dom.minidom.parseString(tostring(root))
        declaration = xml.dom.minidom.Document().toxml()
        return dom.toprettyxml()[len(declaration) + 1:]
