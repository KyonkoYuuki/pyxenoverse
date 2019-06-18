from recordclass import recordclass
import struct

from pyxenoverse.emm.material import Material

EMM_SIGNATURE = b'#EMM'
EMMHeader = recordclass('EMMHeader', [
    'endianess_check',
    'u_06',
    'num_entries',
    'material_base_address',
])
EMM_HEADER_SIZE = 12
EMM_HEADER_BYTE_ORDER = 'HHII'


class EMM:
    def __init__(self, endian='<'):
        self.header = None
        self.endian = endian
        self.filename = ''
        self.mat_count = 0
        self.materials = []

    def load(self, filename):
        with open(filename, 'rb') as f:
            if f.read(4) != EMM_SIGNATURE:
                print("Not a valid EMM file")
                return False
            self.endian = '<' if f.read(2) == b'\xFE\xFF' else '>'
            f.seek(4)
            self.read(f, self.endian)
        self.filename = filename
        return True

    def save(self, filename=None):
        if filename:
            self.filename = filename
        with open(self.filename, 'wb') as f:
            f.write(EMM_SIGNATURE)
            self.write(f, '<')

    def read(self, f, endian):
        self.header = EMMHeader(*struct.unpack(endian + EMM_HEADER_BYTE_ORDER, f.read(EMM_HEADER_SIZE)))
        f.seek(self.header.material_base_address)

        # Read material count
        self.mat_count = struct.unpack(endian + 'I', f.read(4))[0]

        # Read material offsets
        mat_offsets = []
        for n in range(self.mat_count):
            mat_offsets.append(struct.unpack(endian + 'I', f.read(4))[0])

        # Read materials
        self.materials = []
        for offset in mat_offsets:
            f.seek(self.header.material_base_address + offset)
            material = Material()
            material.read(f, endian)
            self.materials.append(material)

    def write(self, f, endian):
        self.mat_count = len(self.materials)
        # Write header
        f.write(struct.pack(endian + EMM_HEADER_BYTE_ORDER, *self.header))
        print(self.header)

        # Goto calculated start of materials
        f.seek(self.header.material_base_address + self.mat_count * 4 + 4)

        # Write Materials
        mat_offsets = []
        for material in self.materials:
            mat_offsets.append(f.tell() - self.header.material_base_address)
            material.write(f, endian)

        # Write size
        f.seek(self.header.material_base_address)
        f.write(struct.pack(endian + 'I', self.mat_count))

        # Write offsets
        for offset in mat_offsets:
            f.write(struct.pack(endian + 'I', offset))
