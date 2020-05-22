import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name

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
