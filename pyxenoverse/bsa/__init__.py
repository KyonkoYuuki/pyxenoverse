#!/usr/bin/python3
import struct
from recordclass import recordclass

from pyxenoverse.bsa.entry import Entry, BSA_ENTRY_HEADER_SIZE

BSA_SIGNATURE = b'#BSA'
BSAHeader = recordclass('BSAHeader', [
    'endianess_check',
    'header_size',
    'i_08',
    'i_12',
    'i_16',
    'num_entries',
    'data_start'
])
BSA_HEADER_SIZE = 20
BSA_HEADER_BYTE_ORDER = 'HHIIHHI'


class BSA:
    def __init__(self, endian='<'):
        self.header = None
        self.endian = endian
        self.entries = []
        self.filename = ''

    def load(self, filename):
        with open(filename, 'rb') as f:
            if f.read(4) != BSA_SIGNATURE:
                print("Not a valid BSA file")
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
            f.write(BSA_SIGNATURE)
            self.write(f, self.endian)

    def read(self, f, endian):
        self.header = BSAHeader(*struct.unpack(endian + BSA_HEADER_BYTE_ORDER, f.read(BSA_HEADER_SIZE)))
        self.entries.clear()
        # print(self.header)
        data_offsets = []
        for i in range(self.header.num_entries):
            data_offsets.append(struct.unpack(endian + "I", f.read(4))[0])

        for i, offset in enumerate(data_offsets):
            entry = Entry(i)
            if offset != 0:
                f.seek(offset)
                entry.read(f, endian)
            self.entries.append(entry)

    def write(self, f, endian):
        self.entries.sort(key=lambda entry: entry.index)
        self.header.num_entries = len(self.entries)
        self.header.data_start = 0x18 if self.header.num_entries else 0
        f.write(struct.pack(endian + BSA_HEADER_BYTE_ORDER, *self.header))

        for i, entry in enumerate(self.entries):
            f.seek(self.header.data_start + i * BSA_ENTRY_HEADER_SIZE)
            entry.write(f, endian)
