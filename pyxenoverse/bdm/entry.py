import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bdm.subentry.type0 import Type0

BDMEntry = recordclass('BDMEntry', ['id'])


class Entry(BaseRecord):
    def __init__(self, sub_entry_type=Type0, entry_id=0):
        super().__init__()
        self.sub_entries = []
        self.sub_entry_type = sub_entry_type
        self.data = BDMEntry(entry_id)
        for i in range(10):
            self.sub_entries.append(self.sub_entry_type())

    def read(self, f, endian):
        self.data = BDMEntry(*struct.unpack(endian + 'I', f.read(4)))
        self.sub_entries = []
        for idx in range(10):
            sub_entry = self.sub_entry_type()
            sub_entry.read(f, endian)
            self.sub_entries.append(sub_entry)

    def write(self, f, endian):
        f.write(struct.pack(endian + 'I', *self.data))
        for sub_entry in self.sub_entries:
            sub_entry.write(f, endian)

    def convert_type1_to_type0(self, type1):
        self.id = type1.id
        for n, sub_entry in enumerate(self.sub_entries):
            sub_entry.convert_type1_to_type0(type1.sub_entries[n])

    def paste(self, other):
        self.sub_entries.clear()
        self.sub_entries.extend(other.sub_entries)
