import re
from recordclass import recordclass
import struct

from pyxenoverse import BaseRecord, read_name
from pyxenoverse.bcs.utils import get_costume_creator_name

from xml.etree.ElementTree import SubElement, Comment

BCSPhysics = recordclass('BCSPhysics', [
    'model',
    'model2',
    'texture',
    'u_06',
    'u_08',
    'u_10',
    'u_14',
    'dyt_options',
    'part_hiding',
    'u_20',
    'name',
    'emd_offset',  # 0x2c
    'emm_offset',
    'emb_offset',
    'esk_offset',
    'bone_offset',
    'scd_offset',
    'u_40'
])

BCS_PHYSICS_XML_TRANSLATION = {
    'model': 'u_00',
    'model2': 'u_02',
    'texture': 'u_04',
    'dyt_options': 'u_18',
    'part_hiding': 'u_1c'
}

BCS_PHYSICS_XML_IGNORE = [
    'u_06',
    'u_08',
    'u_40'
]
BCS_PHYSICS_XML_NAMES = [
    'emd_name',
    'emm_name',
    'emb_name',
    'esk_name',
    'scd_name'
]

BCS_PHYSICS_SIZE = 72
BCS_PHYSICS_BYTE_ORDER = 'HHHHQIIIII4sIIIIIIQ'


class Physics(BaseRecord):
    def __init__(self):
        super().__init__()
        self.emd_name = ''
        self.emm_name = ''
        self.emb_name = ''
        self.esk_name = ''
        self.bone_name = ''
        self.scd_name = ''
        self.data = BCSPhysics(*([0] * len(BCSPhysics.__fields__)))
        self.name = ''

    def read(self, f, endian):
        address = f.tell()
        self.data = BCSPhysics(*struct.unpack(endian + BCS_PHYSICS_BYTE_ORDER, f.read(BCS_PHYSICS_SIZE)))
        self.name = re.sub(r'[^\x20-\x7f]', '', self.name.decode())
        # print(self.data)
        if self.emd_offset:
            self.emd_name = read_name(f, address + self.emd_offset)
            # print(f'emd: {self.emd_name}')
        if self.emm_offset:
            self.emm_name = read_name(f, address + self.emm_offset)
            # print(f'emm: {self.emm_name}')
        if self.emb_offset:
            self.emb_name = read_name(f, address + self.emb_offset)
            # print(f'emb: {self.emb_name}')
        if self.esk_offset:
            self.esk_name = read_name(f, address + self.esk_offset)
            # print(f'esk: {self.esk_name}')
        if self.bone_offset:
            self.bone_name = read_name(f, address + self.bone_offset)
            # print(f'bone: {self.bone_name}')
        if self.scd_offset:
            self.scd_name = read_name(f, address + self.scd_offset)
            # print(f'scd: {self.scd_name}')

    def write(self, f, names, endian):
        address = f.tell()

        self.emd_offset = 0
        self.emm_offset = 0
        self.emb_offset = 0
        self.esk_offset = 0
        self.bone_offset = 0
        self.scd_offset = 0
        if isinstance(self.name, str):
            self.name = self.name.encode()
        f.write(struct.pack(endian + BCS_PHYSICS_BYTE_ORDER, *self.data))

        # Add names
        if self.emd_name:
            names.append((address, 0x28, self.emd_name))
        if self.emm_name:
            names.append((address, 0x2c, self.emm_name))
        if self.emb_name:
            names.append((address, 0x30, self.emb_name))
        if self.esk_name:
            names.append((address, 0x34, self.esk_name))
        if self.bone_name:
            names.append((address, 0x38, self.bone_name))
        if self.scd_name:
            names.append((address, 0x3c, self.scd_name))

    def paste(self, other):
        if type(self) != type(other):
            return False
        self.data = BCSPhysics(*other.data)
        self.emd_name = other.emd_name
        self.emm_name = other.emm_name
        self.emb_name = other.emb_name
        self.esk_name = other.esk_name
        self.bone_name = other.bone_name
        self.scd_name = other.scd_name

        # Replace 3 letter names with current one
        if self.name and other.name:
            self.emd_name = self.emd_name.replace(other.name, self.name)
            self.emm_name = self.emm_name.replace(other.name, self.name)
            self.emb_name = self.emb_name.replace(other.name, self.name)
            self.esk_name = self.esk_name.replace(other.name, self.name)
            self.bone_name = self.bone_name.replace(other.name, self.name)
            self.scd_name = self.scd_name.replace(other.name, self.name)
        return True

    def generate_xml(self, root):
        physics = SubElement(root, "PhysicsObject")
        for field_name in self.data.__fields__:
            if 'num' in field_name or 'offset' in field_name:
                continue
            if field_name in BCS_PHYSICS_XML_IGNORE:
                continue
            xml_name = BCS_PHYSICS_XML_TRANSLATION.get(field_name, field_name).upper()
            if xml_name.startswith("U_"):
                value = hex(self[field_name])
            elif field_name.startswith("model") and self[field_name] < 10000:
                value = "10000"
            else:
                value = str(self[field_name])
            SubElement(physics, xml_name, value=value)

        # Add file names
        physics.append(Comment("MODEL, EMM, EMB, ESK, BONE, SCD"))
        model_names = {}
        for name in BCS_PHYSICS_XML_NAMES:
            model_names[name] = get_costume_creator_name(self[name])
        SubElement(physics, "STR_28", value=f'{model_names["emd_name"] or "NULL"}, {model_names["emm_name"] or "NULL"}, '
                                           f'{model_names["emb_name"] or "NULL"}, {model_names["esk_name"] or "NULL"}, '
                                           f'{self.bone_name or "NULL"}, {model_names["scd_name"] or "NULL"}')
