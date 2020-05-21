import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name

BCSColor = recordclass('BCSColor', [
    'red1',
    'green1',
    'blue1',
    'alpha1',
    'red2',
    'green2',
    'blue2',
    'alpha2',
    'red3',
    'green3',
    'blue3',
    'alpha3',
    'red4',
    'green4',
    'blue4',
    'alpha4',
    'f_40',
    'f_44',
    'f_48',
    'f_4c',

])
BCS_COLOR_SIZE = 80
BCS_COLOR_BYTE_ORDER = 'ffffffffffffffffffff'


class Color(BaseRecord):
    def __init__(self):
        super().__init__()
        self.data = BCSColor(*([0] * len(BCSColor.__fields__)))
        self.color1 = []
        self.color2 = []
        self.color3 = []

    def read(self, f, endian):
        self.data = BCSColor(*struct.unpack(endian + BCS_COLOR_BYTE_ORDER, f.read(BCS_COLOR_SIZE)))
        for i in range(len(self.data)):
            self.data[i] = int(self.data[i] * 255.0)
        self.color1 = [self.red1, self.green1, self.blue1, self.alpha1]
        self.color2 = [self.red2, self.green2, self.blue2, self.alpha2]
        self.color3 = [self.red3, self.green3, self.blue3, self.alpha3]
        self.color4 = [self.red4, self.green4, self.blue4, self.alpha4]

        # print(self.data)

    def write(self, f, endian):
        self.red1, self.green1, self.blue1, self.alpha1 = self.color1
        self.red2, self.green2, self.blue2, self.alpha2 = self.color2
        self.red3, self.green3, self.blue3, self.alpha3 = self.color3
        self.red4, self.green4, self.blue4, self.alpha4 = self.color4
        for i in range(len(self.data)):
            self.data[i] /= 255.0
        f.write(struct.pack(endian + BCS_COLOR_BYTE_ORDER, *self.data))
