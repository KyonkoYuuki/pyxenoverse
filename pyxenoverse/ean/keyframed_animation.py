import math
from recordclass import recordclass
import struct

from pyxenoverse import BaseRecord
from pyxenoverse.ean.keyframe import Keyframe

EANKeyframedAnimation = recordclass(
    'EANKeyframedAnimation', ['keyframes_count', 'indices_offset', 'keyframes_offset'])
EAN_KEYFRAMED_ANIMATION_SIZE = 12
EAN_KEYFRAMED_ANIMATION_BYTE_ORDER = 'III'


def lerp(src, dest, factor):
    return src + factor * (dest - src)


class KeyframedAnimation(BaseRecord):
    def __init__(self):
        self.keyframes = []
        self.flag = 0
        super().__init__()
        self.data = EANKeyframedAnimation(0, 0, 0)

    def read(self, f, index_size, keyframe_size, endian):
        base_keyframed_animation_address = f.tell()
        self.flag = struct.unpack('<I', f.read(4))[0]
        self.data = EANKeyframedAnimation(*struct.unpack(
            endian + EAN_KEYFRAMED_ANIMATION_BYTE_ORDER, f.read(EAN_KEYFRAMED_ANIMATION_SIZE)))
        # print("[{}] flag : {}, keyframes_count : {}, indices_offset : [{}], keyframes_offset : [{}]".format(
        #     base_keyframed_animation_address, self.flag, self.keyframes_count, self.indices_offset, self.keyframes_offset))

        self.keyframes.clear()
        f.seek(base_keyframed_animation_address + self.indices_offset)
        for i in range(self.keyframes_count):
            # print("KF {} : [{}] : ".format(i, f.tell()))
            keyframe = Keyframe()
            keyframe.read_frame(f, index_size, endian)
            self.keyframes.append(keyframe)
        
        f.seek(base_keyframed_animation_address + self.keyframes_offset)
        for i in range(self.keyframes_count):
            # print("KF {} : [{}] : ".format(i, f.tell()))
            self.keyframes[i].read(f, keyframe_size, endian)

    def write(self, f, index_size, keyframe_size, endian):
        base_keyframed_animation_address = f.tell()
        self.keyframes_count = len(self.keyframes)
        self.indices_offset = 16
        self.keyframes_offset = int(math.ceil(
            (base_keyframed_animation_address + self.indices_offset + self.keyframes_count *
             (1 if index_size == 0 else 2)) / 16.0 )) * 16 - base_keyframed_animation_address

        f.write(struct.pack('<I', self.flag))
        f.write(struct.pack(endian + EAN_KEYFRAMED_ANIMATION_BYTE_ORDER, *self.data))
        # print("[{}] flag : {}, keyframes_count : {}, indices_offset : [{}], keyframes_offset : [{}]".format(
        #     base_keyframed_animation_address, self.flag, keyframes_count, indices_offset, keyframes_offset))

        f.seek(base_keyframed_animation_address + self.indices_offset)
        for i, keyframe in enumerate(self.keyframes):
            # print("KF {} : [{}] : ".format(i, f.tell()))
            keyframe.write_frame(f, index_size, endian)

        f.seek(base_keyframed_animation_address + self.keyframes_offset)
        for i, keyframe in enumerate(self.keyframes):
            # print("KF {} : [{}] : ".format(i, f.tell()))
            keyframe.write(f, keyframe_size, endian)

        return self.keyframes_offset + self.keyframes_count * 4 * (2 if keyframe_size == 1 else 4)

    def get_interpolated_frame(self, frame, factor):
        lower_keyframe = None
        upper_keyframe = None
        inter_frame = float(frame) / factor
        for keyframe in sorted(self.keyframes, key=lambda k: k.frame):

            if keyframe.frame < inter_frame:
                lower_keyframe = keyframe

            if keyframe.frame == inter_frame:
                lower_keyframe = upper_keyframe = keyframe
                break

            if keyframe.frame > inter_frame:
                upper_keyframe = keyframe
                break

        # print("frame: {}, lower_frame: {}, upper_frame: {}".format(frame, lower_keyframe.frame, upper_keyframe.frame))
        interpolated_frame = Keyframe()
        interpolated_frame.frame = frame
        if lower_keyframe is None and upper_keyframe is None:
            interpolated_frame.x = 0.0
            interpolated_frame.y = 0.0
            interpolated_frame.z = 0.0
            interpolated_frame.w = 0.0
        elif lower_keyframe == upper_keyframe:
            return None
        elif lower_keyframe is not None and upper_keyframe is not None:
            lower_frame = float(lower_keyframe.frame)
            upper_frame = float(upper_keyframe.frame)
            factor = (inter_frame - lower_frame) / (upper_frame - lower_frame)

            interpolated_frame.x = lerp(lower_keyframe.x, upper_keyframe.x, factor)
            interpolated_frame.y = lerp(lower_keyframe.y, upper_keyframe.y, factor)
            interpolated_frame.z = lerp(lower_keyframe.z, upper_keyframe.z, factor)
            interpolated_frame.w = lerp(lower_keyframe.w, upper_keyframe.w, factor)
        elif lower_keyframe is not None:
            interpolated_frame.x = lower_keyframe.x
            interpolated_frame.y = lower_keyframe.y
            interpolated_frame.z = lower_keyframe.z
            interpolated_frame.w = lower_keyframe.w
        elif upper_keyframe is not None:
            interpolated_frame.x = upper_keyframe.x
            interpolated_frame.y = upper_keyframe.y
            interpolated_frame.z = upper_keyframe.z
            interpolated_frame.w = upper_keyframe.w
        return interpolated_frame
