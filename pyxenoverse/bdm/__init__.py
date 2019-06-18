from recordclass import recordclass
import struct

from pyxenoverse.bdm.entry import Entry
from pyxenoverse.bdm.subentry.type0 import Type0
from pyxenoverse.bdm.subentry.type1 import Type1

BDM_SIGNATURE = b'#BDM'
BDMheader = recordclass('BDMheader', [
    'endianess_check',
    'u_06',
    'num_entries',
    'data_start'
])
BDM_HEADER_SIZE = 12
BDM_HEADER_BYTE_ORDER = 'HHII'


class BDM:
    def __init__(self, endian='<'):
        self.header = None
        self.endian = endian
        self.entries = []
        self.type = Type0
        self.filename = ''

    def load(self, filename):
        with open(filename, 'rb') as f:
            if f.read(4) != BDM_SIGNATURE:
                print("Not a valid BDM file")
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
            f.write(BDM_SIGNATURE)
            self.write(f, '<')

    def read(self, f, endian):
        # header
        self.header = BDMheader(*struct.unpack(endian + BDM_HEADER_BYTE_ORDER, f.read(BDM_HEADER_SIZE)))

        try:
            # Type 0
            self.entries.clear()
            f.seek(self.header.data_start)
            for _ in range(self.header.num_entries):
                entry = Entry(Type0)
                entry.read(f, endian)
                self.entries.append(entry)

        except struct.error:
            # Type 1
            self.entries.clear()
            self.type = Type1
            f.seek(self.header.data_start)
            for _ in range(self.header.num_entries):
                # Read Type1 Entry
                type1 = Entry(Type1)
                type1.read(f, endian)

                # Convert to Type0
                type0 = Entry(Type0)
                type0.convert_type1_to_type0(type1)
                self.entries.append(type0)

    def write(self, f, endian):
        self.header.num_entries = len(self.entries)
        self.header.data_start = 16  # never changes
        f.write(struct.pack(endian + BDM_HEADER_BYTE_ORDER, *self.header))
        f.seek(self.header.data_start)
        for entry in self.entries:
            entry.write(f, endian)
