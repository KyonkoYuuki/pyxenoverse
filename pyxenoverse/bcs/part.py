import struct
import re
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name
from pyxenoverse.bcs.color_selector import ColorSelector, BCS_COLOR_SELECTOR_SIZE
from pyxenoverse.bcs.physics import Physics, BCS_PHYSICS_SIZE

from xml.etree.ElementTree import SubElement, Comment

BCSPart = recordclass('BCSPart', [
    'model',
    'model2',
    'texture',
    'u_06',
    'u_08',
    'u_10',
    'num_color_selectors',
    'color_selector_offset',
    'dyt_options',
    'part_hiding',
    'u_20',
    'f_24',
    'f_28',
    'u_2c',
    'u_30',
    'name',
    'emd_offset',  # 56
    'emm_offset',  # 60
    'emb_offset',  # 64
    'ean_offset',  # 68
    'u_48',
    'num_physics',
    'physics_offset',
    'u_50',
    'num_unk3',
    'unk3_offset'
])

BCS_PART_XML_TRANSLATION = {
    'dyt_options': 'u_18',
    'part_hiding': 'u_1c'
}

BCS_PART_XML_IGNORE = [
    'u_06',
    'u_08',
    'u_48',
    'u_50'
]
BCS_PART_SIZE = 88
BCS_PART_BYTE_ORDER = 'HHHHQHHIIIIffII4sIIIIHHIHHI'


class Part(BaseRecord):
    def __init__(self):
        super().__init__()
        self.color_selectors = []
        self.physics = []
        self.unk3 = []
        self.emd_name = ''
        self.emm_name = ''
        self.emb_name = ''
        self.ean_name = ''
        self.data = BCSPart(*([0] * len(BCSPart.__fields__)))
        self.name = ''

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSPart(*struct.unpack(endian + BCS_PART_BYTE_ORDER, f.read(BCS_PART_SIZE)))
        self.name = re.sub(r'[^\x20-\x7f]', '', self.name.decode())
        # print(self.data)
        if self.emd_offset:
            self.emd_name = read_name(f, address + self.emd_offset)
        if self.emm_offset:
            self.emm_name = read_name(f, address + self.emm_offset)
            # print(f'emm: {self.emm_name}')
        if self.emb_offset:
            self.emb_name = read_name(f, address + self.emb_offset)
            # print(f'emb: {self.emb_name}')
        if self.ean_offset:
            self.ean_name = read_name(f, address + self.ean_offset)
            # print(f'ean: {self.ean_name}')

        # Color Selectors
        self.color_selectors.clear()
        for i in range(self.num_color_selectors):
            f.seek(address + self.color_selector_offset + i * BCS_COLOR_SELECTOR_SIZE)
            color_selector = ColorSelector()
            color_selector.read(f, endian)
            self.color_selectors.append(color_selector)

        # Physics
        self.physics.clear()
        for i in range(self.num_physics):
            f.seek(address + self.physics_offset + i * BCS_PHYSICS_SIZE)
            physics = Physics()
            physics.read(f, endian)
            self.physics.append(physics)

        # Unk3 Hack
        self.unk3.clear()
        if self.num_unk3:
            f.seek(address + self.unk3_offset)
            unk3_start_address = f.tell()
            i = 0
            while i < self.num_unk3:
                unk3 = struct.unpack(endian + "I", f.read(4))[0]
                if unk3 == 8:
                    i += 1

            unk3 = struct.unpack(endian + "I", f.read(4))[0]

            while True:
                h1 = unk3 & 0xFFFF
                h2 = unk3 >> 16
                unk3 = struct.unpack(endian + "I", f.read(4))[0]
                if h1 != h2:
                    break
            unk3_end_address = f.tell() - 4  # remove a byte
            unk3_length = unk3_end_address - unk3_start_address
            f.seek(unk3_start_address)
            self.unk3 = list(struct.unpack(endian + unk3_length * "B", f.read(unk3_length)))
            # print(self.unk3)

    def write(self, f, names, endian):
        start_address = f.tell()

        if isinstance(self.name, str):
            self.name = self.name.encode()

        # Reset offsets to 0
        self.emd_offset = 0
        self.emm_offset = 0
        self.emb_offset = 0
        self.ean_offset = 0
        self.color_selectors_offset = 0
        self.physics_offset = 0
        self.unk3_offset = 0

        # Add names
        if self.emd_name:
            names.append((start_address, 0x38, self.emd_name))
        if self.emm_name:
            names.append((start_address, 0x3c, self.emm_name))
        if self.emb_name:
            names.append((start_address, 0x40, self.emb_name))
        if self.ean_name:
            names.append((start_address, 0x44, self.ean_name))

        # Set lengths
        self.num_color_selectors = len(self.color_selectors)
        self.num_physics = len(self.physics)
        unk3_length = len(self.unk3)
        f.seek(start_address + BCS_PART_SIZE)

        # Color Selectors
        if self.num_color_selectors:
            self.color_selector_offset = f.tell() - start_address
            for i, color_selector in enumerate(self.color_selectors):
                f.seek(start_address + self.color_selector_offset + i * BCS_COLOR_SELECTOR_SIZE)
                color_selector.write(f, endian)

        # Physics
        if self.num_physics:
            self.physics_offset = f.tell() - start_address
            for i, physics in enumerate(self.physics):
                f.seek(start_address + self.physics_offset + i * BCS_PHYSICS_SIZE)
                physics.write(f, names, endian)

        # Unk3
        if unk3_length:
            self.unk3_offset = f.tell() - start_address
            f.seek(start_address + self.unk3_offset)
            f.write(struct.pack(endian + unk3_length * "B", *self.unk3))

        # Write Part header
        end_address = f.tell()
        f.seek(start_address)
        f.write(struct.pack(endian + BCS_PART_BYTE_ORDER, *self.data))
        f.seek(end_address)

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSPart(*other.data)
        self.color_selectors = other.color_selectors.copy()
        self.physics = other.physics.copy()
        self.unk3 = other.unk3.copy()

        self.emd_name = other.emd_name
        self.emm_name = other.emm_name
        self.emb_name = other.emb_name
        self.ean_name = other.ean_name

        # Replace 3 letter names with current one
        if self.name and other.name:
            self.emd_name = self.emd_name.replace(other.name, self.name)
            self.emm_name = self.emm_name.replace(other.name, self.name)
            self.emb_name = self.emb_name.replace(other.name, self.name)
            self.ean_name = self.ean_name.replace(other.name, self.name)
        return True

    def paste_color_selectors(self, other, append):
        if not isinstance(other, list):
            return False
        if not isinstance(other[0], ColorSelector):
            return False

        if append:
            self.color_selectors.extend(other.copy())
        else:
            self.color_selectors = other.copy()

    def paste_physics(self, other, append):
        if not isinstance(other, list):
            return False
        if not isinstance(other[0], Physics):
            return False

        if append:
            self.physics.extend(other.copy())
        else:
            self.physics = other.copy()

    def generate_xml(self, root, part_colors=None):
        for field_name in self.data.__fields__:
            if 'num' in field_name or 'offset' in field_name:
                continue
            if field_name in BCS_PART_XML_IGNORE:
                continue
            xml_name = BCS_PART_XML_TRANSLATION.get(field_name, field_name).upper()
            if xml_name.startswith("U_"):
                value = hex(self[field_name])
            else:
                value = str(self[field_name])
            SubElement(root, xml_name, value=value)

        # Add file names
        root.append(Comment("MODEL, EMM, EMB, EAN"))
        SubElement(root, "FILES", value=f'{self.emd_name or "NULL"}, {self.emm_name or "NULL"}, '
                                        f'{self.emb_name or "NULL"}, {self.ean_name or "NULL"}')

        # Add Color Selectors
        for cs in self.color_selectors:
            cs.generate_xml(root, part_colors)

        # Add Physics
        for p in self.physics:
            p.generate_xml(root)

