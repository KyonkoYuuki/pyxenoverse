#!/usr/bin/python3
import math
import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord, read_name, write_name
from pyxenoverse.esk import ESK
from pyxenoverse.ean.animation import Animation

LIBXENOVERSE_EAN_SIGNATURE = b'#EAN'
EANHeader = recordclass('EANHeader', [
    'endianess_check',
    'unk_06',
    'unknown_total',
    'unk_0c',
    'unk_10',
    'animation_type',
    'animation_count',
    'skeleton_offset',
    'animation_keyframes_offset',
    'animation_names_offset'
])
EAN_HEADER_SIZE = 28
EAN_HEADER_BYTE_ORDER = 'HHIIBBHIII'


class EAN(BaseRecord):
    def __init__(self, endian='<'):
        self.endian = endian
        self.skeleton = None
        self.animations = []
        self.filename = ''
        super().__init__()

    def load(self, filename):
        with open(filename, 'rb') as f:
            if f.read(4) != LIBXENOVERSE_EAN_SIGNATURE:
                return False
            self.endian = '<' if f.read(2) == b'\xFE\xFF' else '>'
            f.seek(len(LIBXENOVERSE_EAN_SIGNATURE))
            self.read(f, self.endian)
        self.filename = filename
        return True

    def save(self, filename=None):
        if filename:
            self.filename = filename
        with open(self.filename, 'wb') as f:
            f.write(LIBXENOVERSE_EAN_SIGNATURE)
            return self.write(f, '<')

    def read(self, f, endian):
        self.data = EANHeader(*struct.unpack(endian + EAN_HEADER_BYTE_ORDER, f.read(EAN_HEADER_SIZE)))
        # print("--------------- read EAN \n[8] unkTotal : {}, animation_count : {}, SkeletonOffset : [{}]"
        #       " animation_keyframes_offset : [{}], animation_names_offset : [{}]".format(
        #           self.unknown_total, self.animation_count, self.skeleton_offset, self.animation_keyframes_offset,
        #           self.animation_names_offset))

        # Read Skeleton
        # print("----------- Skeleton")
        f.seek(self.skeleton_offset)
        self.skeleton = ESK(endian)
        self.skeleton.read(f, endian)

        # Read Animations
        # print("----------- Animations KeyFrames")
        self.animations.clear()
        for i in range(self.animation_count):
            animation = Animation(self)
            # Read Keyframes
            f.seek(self.animation_keyframes_offset + i * 4)
            address = struct.unpack(endian + 'I', f.read(4))[0]
            f.seek(address)
            # print("------ animation {} : [{}] => [{}]".format(i, self.animation_keyframes_offset + i * 4, address))
            animation.read(f, endian)

            # Read Name
            f.seek(self.animation_names_offset + i * 4)
            address = struct.unpack(endian + 'I', f.read(4))[0]
            f.seek(address)
            animation.name = read_name(f)
            # print("------ animation {} : [{}] => [{}] => {}".format(
            #     i, self.animation_names_offset + i * 4, address, animation.get_name()))

            self.animations.append(animation)

    def write(self, f, endian):
        removed_nodes = self.clean_animations()
        self.animation_count = len(self.animations)

        # different parts of the file
        self.skeleton_offset = EAN_HEADER_SIZE + len(LIBXENOVERSE_EAN_SIGNATURE)

        # Write Skeleton
        f.seek(self.skeleton_offset)
        self.skeleton.write(f, endian, False)

        # Write Animations
        self.animation_keyframes_offset = f.tell()
        # print("----------- Animations KeyFrames - animation_keyframes_offset : [{}]".format(
        #     self.animation_keyframes_offset))
        keyframe_size = 0
        address_start_keyframe_def = math.ceil((self.animation_keyframes_offset + self.animation_count * 4) / 16.0) * 16

        for i, animation in enumerate(self.animations):
            # Write Keyframes
            f.seek(self.animation_keyframes_offset + i * 4)
            address = address_start_keyframe_def + keyframe_size
            f.write(struct.pack(endian + 'I', address))
            f.seek(address)

            # print("------ animation {} : [{}] => [{}]".format(i, animation_keyframes_offset + i * 4, address))

            animation.set_parent(self)
            current_keyframe_size = animation.write(f, endian)

            # fill zero on end of 16 octet lines
            size_to_fill = (math.ceil(current_keyframe_size / 16.0) * 16) - current_keyframe_size
            # print('current_keyframe_size: {}, size_to_fill: {}'.format(current_keyframe_size, size_to_fill))
            if size_to_fill:
                f.write(b'\x00' * size_to_fill)
                current_keyframe_size += size_to_fill
            keyframe_size += current_keyframe_size

            if i + 1 != self.animation_count:
                f.write(b'\x00' * 16)
                keyframe_size += 16

        f.write(b'\x00' * 12)
        keyframe_size += 12

        # Write Animation Names
        self.animation_names_offset = f.tell()
        # print("----------- Animations Names - animation_names_offset : [{}]".format(self.animation_names_offset))

        names_size = 0
        for i, animation in enumerate(self.animations):
            f.seek(self.animation_names_offset + i * 4)
            address = self.animation_names_offset + self.animation_count * 4 + names_size
            f.write(struct.pack(endian + 'I', address))
            f.seek(address)
            write_name(f, animation.name)
            names_size += len(animation.name) + 1

        # Now we have offsets for everything, lets write the header
        f.seek(len(LIBXENOVERSE_EAN_SIGNATURE))
        f.write(struct.pack(EAN_HEADER_BYTE_ORDER, *self.data))
        # print("-------------- write EAN \n[8] unkTotal : {}, animation_count : {}, SkeletonOffset : [{}],
        #       " animation_keyframes_offset : [{}], animation_names_offset : [{}]".format(
        #           self.unknown_total, self.animation_count, self.skeleton_offset, self.animation_keyframes_offset,
        #           self.animation_names_offset))
        return removed_nodes

    def get_bone_difference(self, other):
        return self.skeleton.get_bone_difference(other.skeleton)

    def clean_animations(self):
        removed_nodes = set()
        for animation in self.animations:
            removed_nodes.update(animation.clean_nodes())
        return removed_nodes

    def remove_animation(self, i):
        del(self.animations[i])
