import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.emm.parameter import Parameter


EMMMaterial = recordclass('EMMMaterial', ['name', 'shader_name', 'param_count', 'u_42'])
EMM_MATERIAL_SIZE = 68
EMM_MATERIAL_BYTE_ORDER = '32s32sHH'


class Material(BaseRecord):
    def __init__(self):
        self.parameters = []
        super().__init__()
        self.data = EMMMaterial('', '', 0, 0)

    def read(self, f, endian):
        self.data = EMMMaterial(*struct.unpack(endian + EMM_MATERIAL_BYTE_ORDER, f.read(EMM_MATERIAL_SIZE)))
        self.name = self.name.decode().rstrip('\0')
        self.shader_name = self.shader_name.decode().rstrip('\0')
        self.parameters = []
        print(self)
        for n in range(self.param_count):
            param = Parameter()
            param.read(f, endian)
            self.parameters.append(param)

    def write(self, f, endian):
        self.param_count = len(self.parameters)
        self.name = self.name.ljust(32, '\0').encode()
        self.shader_name = self.shader_name.ljust(32, '\0').encode()
        f.write(struct.pack(endian + EMM_MATERIAL_BYTE_ORDER, *self.data))
        for param in self.parameters:
            param.write(f, endian)
