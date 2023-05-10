import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.bsa.collision import Collision
from pyxenoverse.bsa.expiration import Expiration
from pyxenoverse.bsa.types.entry_passing import EntryPassing
from pyxenoverse.bsa.types.movement import Movement
from pyxenoverse.bsa.types.type2 import Type2
from pyxenoverse.bsa.types.hitbox import Hitbox
from pyxenoverse.bsa.types.deflection import Deflection
from pyxenoverse.bsa.types.effect import Effect
from pyxenoverse.bsa.types.sound import Sound
from pyxenoverse.bsa.types.screen_effect import ScreenEffect
from pyxenoverse.bsa.types.type10 import Type10
from pyxenoverse.bsa.types.type12 import Type12
from pyxenoverse.bsa.types.type13 import Type13
ITEM_TYPES = {
    -2: Collision,
    -1: Expiration,
    0: EntryPassing,
    1: Movement,
    2: Type2,
    3: Hitbox,
    4: Deflection,
    # 5 doesn't exist?
    6: Effect,
    7: Sound,
    8: ScreenEffect,
    10: Type10,
    12: Type12,
    13: Type13
}

BSASubEntry = recordclass('BSASubEntry', [
    'type',
    'i_02',
    'i_04',
    'count',
    'duration_offset',
    'data_start'
])

BSA_SUB_ENTRY_SIZE = 16
BSA_SUB_ENTRY_BYTE_ORDER = "HHHHII"

BSADuration = recordclass('BSADuration', [
    'start_time',
    'end_time'
])

BSA_DURATION_SIZE = 4
BSA_DURATION_BYTE_ORDER = "HH"


class SubEntry(BaseRecord):
    def __init__(self, index=0):
        super().__init__()
        self.index = index
        self.offset = 0
        self.sub_entry = None
        self.items = []
        self.data = BSASubEntry(*([0] * len(BSASubEntry.__fields__)))

    def read(self, f, endian):
        self.offset = f.tell()
        self.data = BSASubEntry(*struct.unpack(endian + BSA_SUB_ENTRY_BYTE_ORDER, f.read(BSA_SUB_ENTRY_SIZE)))
        # print(self.data)

    def read_items(self, f, endian):

        # Read items
        self.items = []
        item_type = ITEM_TYPES[self.type]
        if not self.count:
            return
        f.seek(self.offset + self.data_start)
        for n in range(self.count):
            item = item_type(n)
            item.read(f, endian)
            self.items.append(item)

        f.seek(self.offset + self.duration_offset)
        for item in self.items:
            item.read_duration(f, endian)
            # print(f'start_time={item.start_time}, duration={item.duration}, {item.data}')

    def write(self, f, endian):
        self.count = len(self.items)
        f.write(struct.pack(endian + BSA_SUB_ENTRY_BYTE_ORDER, *self.data))

    def write_items(self, f, endian, data_start):
        self.duration_offset = f.tell() - data_start
        for item in self.items:
            item.write_duration(f, endian)
        self.data_start = f.tell() - data_start
        for item in self.items:
            item.write(f, endian)

    def paste(self, other):
        if type(self) != type(other):
            return False
        if self.type != other.type:
            return False
        self.data = BSASubEntry(*other.data)
        self.items = other.items.copy()
        return True

    def get_readable_name(self):
        return ITEM_TYPES[self.type].__name__ + ' Group'

    def get_type_name(self):
        return ITEM_TYPES[self.type].__name__
