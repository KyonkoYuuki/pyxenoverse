import struct

from pyxenoverse import BaseRecord


# Type 0
class BaseType(BaseRecord):
    description = {}
    description_type = None

    def __init__(self, index):
        super().__init__()
        self.index = index
        self.data = self.bac_record(*([0] * len(self.bac_record.__fields__)))

    def get_size(self, type17_small):
        return self.size

    def read(self, f, endian, _):
        self.data = self.bac_record(*struct.unpack(endian + self.byte_order, f.read(self.size)))

    def write(self, f, endian):
        f.write(struct.pack(endian + self.byte_order, *self.data))

    def replace_values(self, changed_values):
        if type(self) not in changed_values:
            return
        changed = changed_values[type(self)]
        for key_pair, v in changed.items():
            entry = key_pair[0]
            dependency = key_pair[1]
            for depend_value, values in v.items():
                for old_value, new_value in values.items():
                    if new_value is None:
                        continue
                    elif (not dependency or self[dependency] == depend_value) and self[entry] == old_value:
                        self[entry] = new_value
                        break

    def paste(self, other, changed_values={}):
        if type(self) != type(other):
            return False

        self.data = self.bac_record(*other.data)
        self.replace_values(changed_values)
        return True

    def get_static_values(self):
        static_values = {}
        for key_pair, values in self.dependencies.items():
            entry = key_pair[0]
            dependency = key_pair[1]
            if not dependency:
                static_values[key_pair] = {None:  {self[entry]}}
            elif self[dependency] in values:
                static_values[key_pair] = {self[dependency]:  {self[entry]}}
        if not static_values:
            return {}
        return {type(self): static_values}
