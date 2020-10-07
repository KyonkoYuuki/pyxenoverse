from collections import defaultdict
import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bsa.collision import Collision
from pyxenoverse.bsa.expiration import Expiration
from pyxenoverse.bsa.sub_entry import SubEntry

BSAEntry = recordclass('BSAEntry', [
    'i_00',
    'collision_count',
    'expiration_count',
    'collision_offset',
    'expiration_offset',
    'impact_properties',
    'i_17',
    'i_18',
    'lifetime',
    'i_24',
    'expires',
    'impact_projectile',
    'impact_enemy',
    'impact_ground',
    'sub_entry_count',
    'sub_entry_offset',
    'i_40',
    'i_44',
    'i_48',
])


BSA_ENTRY_HEADER_SIZE = 52
BSA_ENTRY_HEADER_BYTE_ORDER = 'IHHIIBBIHHHHHHHIIII'


class Entry(BaseRecord):
    def __init__(self, index=0):
        super().__init__()
        self.index = index
        self.collisions = []
        self.expirations = []
        self.sub_entries = []
        self.data = BSAEntry(*([0] * len(BSAEntry.__fields__)))

    def read(self, f, endian):
        self.data = BSAEntry(*struct.unpack(endian + BSA_ENTRY_HEADER_BYTE_ORDER, f.read(BSA_ENTRY_HEADER_SIZE)))
        # print(self.data)
        for _ in range(self.collision_count):
            collision = Collision()
            collision.read(f, endian)
            self.collisions.append(collision)

        for _ in range(self.expiration_count):
            expiration = Expiration()
            expiration.read(f, endian)
            self.expirations.append(expiration)

        self.sub_entries = []
        for n in range(self.sub_entry_count):
            sub_entry = SubEntry(n)
            sub_entry.read(f, endian)
            self.sub_entries.append(sub_entry)

        for sub_entry in self.sub_entries:
            sub_entry.read_items(f, endian)

    def write(self, f, endian):
        f.write(struct.pack(endian + 'I', *self.data))
        for sub_entry in self.sub_entries:
            sub_entry.write(f, endian)

    def paste(self, other):
        pass
