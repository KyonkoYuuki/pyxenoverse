#!/usr/bin/python3
import struct

from recordclass import recordclass
from pyxenoverse import BaseRecord, merge_dict

BACEntry = recordclass('BACEntry', [
    'flags',
    'num_sub_entries',
    'unk_06',
    'sub_entry_offset',
    'unk_0C'
])
BAC_ENTRY_SIZE = 16
BAC_ENTRY_BYTE_ORDER = 'IHHII'


class Entry(BaseRecord):
    def __init__(self, bac, index):
        super().__init__()
        self.bac = bac
        self.index = index
        self.sub_entries = []
        self.data = BACEntry(*([0] * len(BACEntry.__attrs__)))
        self.flags = 0x80000000

    def read(self, f, endian):
        self.data = BACEntry(*struct.unpack(endian + BAC_ENTRY_BYTE_ORDER, f.read(BAC_ENTRY_SIZE)))
        # self.flags = self.flags & 0xF if self.num_sub_entries > 0 else (self.flags & 0x0F) | 0x80000000

    def write(self, f, sub_entry_offset, item_offset, endian):
        self.sub_entries.sort(key=lambda n: n.type)
        self.num_sub_entries = len(self.sub_entries)
        if self.num_sub_entries:
            self.sub_entry_offset = sub_entry_offset
        else:
            self.sub_entry_offset = 0
        f.write(struct.pack(endian + BAC_ENTRY_BYTE_ORDER, *self.data))
        for i, sub_entry in enumerate(self.sub_entries):
            f.seek(sub_entry_offset)
            item_offset = sub_entry.write(f, item_offset, endian)
            sub_entry_offset += 16
        return sub_entry_offset, item_offset

    def paste(self, other, changed_values={}, copy_sub_entries=True):
        if type(self) != type(other):
            return False
        self.data = BACEntry(*other.data)
        if copy_sub_entries:
            self.sub_entries = other.sub_entries.copy()
            for sub_entry in self.sub_entries:
                for item in sub_entry.items:
                    item.replace_values(changed_values)
        return True

    def get_static_values(self):
        static_values = {}
        for sub_entry in self.sub_entries:
            merge_dict(static_values, sub_entry.get_static_values())
        return static_values
