#!/usr/bin/python3
import struct
from recordclass import recordclass

from pyxenoverse.bac.entry import Entry
from pyxenoverse.bac.sub_entry import SubEntry

BAC_SIGNATURE = b'#BAC'

BACHeader = recordclass('BACHeader', [
    'endianess_check',
    'u_06',
    'num_entries',
    'u_0c',
    'data_start',
    'u_14', 'u_18', 'u_1c',
    'f_20', 'f_24', 'f_28', 'f_2c', 'f_30', 'f_34', 'f_38', 'f_3c', 'f_40', 'f_44', 'f_48', 'f_4c',
    'u_50', 'u_54', 'u_58', 'u_5c'
])
BAC_HEADER_SIZE = 92
BAC_HEADER_BYTE_ORDER = 'HHIIIIIIffffffffffffIIII'


class BAC:
    def __init__(self, endian='<'):
        self.header = None
        self.endian = endian
        self.entries = []
        self.filename = ''

    def load(self, filename):
        with open(filename, 'rb') as f:
            if f.read(4) != BAC_SIGNATURE:
                print("Not a valid BAC file")
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
            f.write(BAC_SIGNATURE)
            self.write(f, self.endian)

    def read(self, f, endian):
        self.header = BACHeader(*struct.unpack(endian + BAC_HEADER_BYTE_ORDER, f.read(BAC_HEADER_SIZE)))
        self.entries.clear()
        for i in range(self.header.num_entries):
            entry = Entry(self, i)
            f.seek(self.header.data_start + i * 16)
            entry.read(f, endian)
            self.entries.append(entry)

        sub_entry_offset = [entry.sub_entry_offset for entry in self.entries if entry.sub_entry_offset][0]
        num_sub_entries = sum(entry.num_sub_entries for entry in self.entries)
        # print(f'num_sub_entries={num_sub_entries}')
        type17_small = False
        type17_found = False
        type17_entry = None
        index = 0
        for i in range(num_sub_entries):
            f.seek(sub_entry_offset + i * 16)
            sub_entry = SubEntry(0)
            sub_entry.read(f, endian)

            # Get size of Throw Handler
            if not type17_found:
                if not type17_entry and sub_entry.type == 17:
                    type17_entry = sub_entry
                elif type17_entry:
                    size = int((sub_entry.offset - type17_entry.offset) / type17_entry.num)
                    if size == 0x14:
                        type17_small = True
                    type17_found = True
            sub_entry.read_items(f, endian, type17_small)
            while len(self.entries[index].sub_entries) >= self.entries[index].num_sub_entries:
                index += 1
            self.entries[index].sub_entries.append(sub_entry)

    def write(self, f, endian):
        self.entries.sort(key=lambda entry: entry.index)
        self.header.num_entries = len(self.entries)
        self.header.data_start = 0x60 # This will never change
        f.write(struct.pack(endian + BAC_HEADER_BYTE_ORDER, *self.header))
        entry_offset = self.header.data_start
        sub_entry_offset = entry_offset + 16 * len(self.entries)
        item_offset = sub_entry_offset + 16 * sum(len(entry.sub_entries) for entry in self.entries)

        for i, entry in enumerate(self.entries):
            f.seek(entry_offset)
            sub_entry_offset, item_offset = entry.write(f, sub_entry_offset, item_offset, endian)
            entry_offset += 16