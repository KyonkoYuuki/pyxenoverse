import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.ean.keyframed_animation import KeyframedAnimation

EANAnimationNode = recordclass(
    'EANAnimationNode', ['bone_index', 'keyframed_animation_count', 'keyframed_animation_offset'])
EAN_ANIMATION_NODE_SIZE = 8
EAN_ANIMATION_NODE_BYTE_ORDER = 'HHI'


class AnimationNode(BaseRecord):
    def __init__(self, ean):
        self.parent = ean
        self.bone_name = ''
        self.keyframed_animations = []
        super().__init__()
        self.data = EANAnimationNode(0, 0, 0)

    def read(self, f, index_size, keyframe_size, endian):
        base_animation_node_address = f.tell()
        self.data = EANAnimationNode(*struct.unpack(endian + EAN_ANIMATION_NODE_BYTE_ORDER, f.read(EAN_ANIMATION_NODE_SIZE)))
        self.bone_name = self.parent.skeleton.bones[self.bone_index].name

        # print("[{}] bone_index : {}, keyframed_animation_count : {}, keyframed_animation_offset : [{}]".format(
        #     base_animation_node_address, self.bone_index, keyframed_animation_count, keyframed_animation_offset))

        self.keyframed_animations.clear()
        for i in range(self.keyframed_animation_count):
            keyframed_animation = KeyframedAnimation()
            f.seek(base_animation_node_address + self.keyframed_animation_offset + i * 4)
            address = struct.unpack(endian + 'I', f.read(4))[0]
            f.seek(base_animation_node_address + address)
            # print("-- KFanim {} : [{}] = {} => [{}]".format(
            #     i, base_animation_node_address + keyframed_animation_offset + i * 4,
            #     address, base_animation_node_address + address))

            keyframed_animation.read(f, index_size, keyframe_size, endian)
            self.keyframed_animations.append(keyframed_animation)

    def write(self, f, index_size, keyframe_size, endian):
        base_animation_node_address = f.tell()
        self.keyframed_animation_count = len(self.keyframed_animations)
        self.keyframed_animation_offset = 8
        f.write(struct.pack(endian + EAN_ANIMATION_NODE_BYTE_ORDER, *self.data))

        # print("[{}] bone_index : {}, keyframed_animation_count : {}, keyframed_animation_offset : [{}]".format(
        #     base_animation_node_address, self.bone_index, keyframed_animation_count, keyframed_animation_offset))

        keyframed_animation_size = 0
        for i, keyframed_animation in enumerate(self.keyframed_animations):
            f.seek(base_animation_node_address + self.keyframed_animation_offset + i * 4)
            address = self.keyframed_animation_offset + self.keyframed_animation_count * 4 + keyframed_animation_size
            f.write(struct.pack(endian + 'I', address))
            f.seek(base_animation_node_address + address)

            # print("-- KFanim {} : [{}] = {} => [{}]".format(
            #     i, base_animation_node_address + keyframed_animation_offset + i * 4,
            #     address, base_animation_node_address + address))

            keyframed_animation_size += keyframed_animation.write(f, index_size, keyframe_size, endian)
        return self.keyframed_animation_offset + self.keyframed_animation_count * 4 + keyframed_animation_size

    def clean_node_for_duration(self, duration):
        if not duration:
            return

        for keyframed_animation in self.keyframed_animations:
            for i, keyframe in reversed(list(enumerate(keyframed_animation.keyframes))):
                if i == 0 or i == len(keyframed_animation.keyframes) - 1:
                    continue
                if keyframe.data == keyframed_animation.keyframes[i-1].data \
                        and keyframe.data == keyframed_animation.keyframes[i+1].data:
                    del keyframed_animation.keyframes[i]
