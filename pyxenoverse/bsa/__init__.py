#!/usr/bin/python3
import os
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
        self.has_comments = False
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

    def loadComment(self, filename):
        #comment

        filename = filename[0:-4]
        filename = filename + "_BSA.cmnt"

        if not os.path.exists(filename):
            #print("does not exists")
            return

        print(self.entries)
        try:
            with open(filename, 'r') as f:
                comments = f.readlines()
                self.has_comments = True
                if self.entries:
                    for i, entry in enumerate(self.entries):
                        entry.setComment(comments[i])
        except:
            print("failed to load comment data, file might be empty or incorrectly formatted")
            return



    def saveComment(self, fileName=None):
        if not self.has_comments:
            return
        fileName = fileName[0:-4]
        fileName = fileName + "_BSA.cmnt"
        cmnt_list = []
        try:
            with open(fileName, 'w') as f:
                for entry in self.entries:

                    cmnt_list.append(entry.getComment() + "\n")
                f.writelines(cmnt_list)
        except:
            print("failed to save comment data")
            return


    def read(self, f, endian):
        self.header = BSAHeader(*struct.unpack(endian + BSA_HEADER_BYTE_ORDER, f.read(BSA_HEADER_SIZE)))
        self.entries.clear()
        # print(self.header)
        data_offsets = []
        for i in range(self.header.num_entries):
            data_offsets.append(struct.unpack(endian + "I", f.read(4))[0])

        # print(data_offsets)
        for i, offset in enumerate(data_offsets):
            if offset == 0:
                continue
            entry = Entry(i)
            f.seek(offset)
            entry.read(f, endian)
            self.entries.append(entry)



    def write(self, f, endian):
        self.entries.sort(key=lambda entry: entry.index)
        self.header.num_entries = self.entries[-1].index + 1
        self.header.data_start = 0x18 if self.header.num_entries else 0
        f.write(struct.pack(endian + BSA_HEADER_BYTE_ORDER, *self.header))

        offsets = [0] * self.header.num_entries
        # print(len(offsets))
        f.seek(self.header.data_start + 4 * self.header.num_entries)

        for entry in self.entries:
            offsets[entry.index] = f.tell()
            entry.write(f, endian)

        f.seek(self.header.data_start)
        for offset in offsets:
            f.write(struct.pack(endian + "I", offset))
