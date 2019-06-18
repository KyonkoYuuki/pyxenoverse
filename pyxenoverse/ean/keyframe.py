import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord

EANKeyframe = recordclass('EANKeyframe', ['x', 'y', 'z', 'w'])


class Keyframe(BaseRecord):
    def __init__(self, frame=0, w=0, x=0, y=0, z=0):
        self.frame = frame
        super().__init__()
        self.data = EANKeyframe(x, y, z, w)

    def __lt__(self, other):
        return self.frame < other.frame

    def paste(self, other):
        self.data = EANKeyframe(*other.data)

    def read(self, f, keyframe_size, endian):
        if keyframe_size == 1:
            self.data = EANKeyframe(*struct.unpack(endian + 'eeee', f.read(8)))
        else:
            self.data = EANKeyframe(*struct.unpack(endian + 'ffff', f.read(16)))
        # print(" (keyframe_size:{}) X : {}, Y : {}, Z : {}, W : {}".format(
        #     keyframe_size, self.x, self.y, self.z, self.w))

    def write(self, f, keyframe_size, endian):
        if keyframe_size == 1:
            f.write(struct.pack(endian + 'eeee', *self.data))
        elif keyframe_size == 2:
            f.write(struct.pack(endian + 'ffff', *self.data))
        else:
            print("Unknown Keyframe Size: {}".format(keyframe_size))
        # print(" (keyframe_size:{}) X : {}, Y : {}, Z : {}, W : {}.".format(
        #     keyframe_size, self.x, self.y, self.z, self.w))

    def read_frame(self, f, index_size, endian):
        if index_size == 0:
            self.frame = struct.unpack(endian + 'B', f.read(1))[0]
        elif index_size == 1:
            self.frame = struct.unpack(endian + 'H', f.read(2))[0]
        else:
            print("Unknown Frame Index Size: {}".format(index_size))
        # print(" (index_size: {}) frame : {}".format(index_size, self.frame))

    def write_frame(self, f, index_size, endian):
        if not index_size:
            if self.frame >= 256:
                print("index of a frame {} is up to a octet (256) limit. please update frameCount".format(self.frame))

            f.write(struct.pack(endian + 'B', self.frame))
        elif index_size == 1:
            f.write(struct.pack(endian + 'H', self.frame))
        else:
            print("Unknown Frame Index Size: {}".format(index_size))
        # print(" (index_size:{}) frame : {}".format(index_size, self.frame))
