import struct
from recordclass import recordclass

from pyxenoverse import BaseRecord
from pyxenoverse.ean.animation_node import AnimationNode
from pyxenoverse.ean.keyframe import Keyframe

EANAnimation = recordclass('EANAnimation', [
    'unk_00',
    'frame_index_size',
    'frame_float_size',
    'frame_count',
    'nodes_count',
    'nodes_offset'
])
EAN_ANIMATION_SIZE = 16
EAN_ANIMATION_BYTE_ORDER = 'HBBIII'


class Animation(BaseRecord):
    def __init__(self, ean):
        self.name = ''
        self.nodes = []
        self.parent = ean
        super().__init__()
        self.data = EANAnimation(0, 0, 0, 0, 0, 0)

    def read(self, f, endian):
        base_animation_address = f.tell()
        self.data = EANAnimation(*struct.unpack(endian + EAN_ANIMATION_BYTE_ORDER, f.read(EAN_ANIMATION_SIZE)))
        # print("[{}] frame_index_size : {}, frame_float_size : {}, frame_count : {}, nodes_count : {}, "
        #       "nodes_offset : [{}]".format(
        #           base_animation_address, self.frame_index_size, self.frame_float_size, self.frame_count,
        #           self.nodes_count, self.nodes_offset))
        self.nodes.clear()
        for i in range(self.nodes_count):
            node = AnimationNode(self.parent)
            f.seek(base_animation_address + self.nodes_offset + i * 4)
            address = struct.unpack(endian + 'I', f.read(4))[0]
            f.seek(base_animation_address + address)
            # print("---- Node {} : [{}] = {} => [{}]".format(
            #     i, base_animation_address + nodes_offset + i * 4, address, base_animation_address + address))
            node.read(f, self.frame_index_size, self.frame_float_size, endian)
            self.nodes.append(node)

    def write(self, f, endian):
        base_animation_address = f.tell()
        self.frame_index_size = 1 if self.frame_count > 255 else 0
        self.nodes_count = len(self.nodes)
        self.nodes_offset = 16
        f.write(struct.pack(endian + EAN_ANIMATION_BYTE_ORDER, *self.data))
        # print("[{}] frame_index_size : {}, frame_float_size : {}, frame_count : {}, nodes_count : {},
        #       "nodes_offset : [{}]".format(
        #           base_animation_address, self.frame_index_size, self.frame_float_size, self.frame_count,
        #           self.nodes_count, self.nodes_offset))

        nodes_size = 0
        for i, node in enumerate(self.nodes):
            # node.clean_animation_for_duration(self.frame_count)
            f.seek(base_animation_address + self.nodes_offset + i * 4)
            address = nodes_size + self.nodes_offset + self.nodes_count * 4
            f.write(struct.pack(endian + 'I', address))
            f.seek(base_animation_address + address)

            # print("---- Node {} : [{}] = {} => [{}]".format(
            #     i, base_animation_address + nodes_offset + i * 4, address, base_animation_address + address))
            nodes_size += node.write(f, self.frame_index_size, self.frame_float_size, endian)

        return self.nodes_offset + self.nodes_count * 4 + nodes_size

    def paste(self, source, bone_filters=None, keep_name=False):
        skeleton_dest = self.parent.skeleton
        skeleton_src = source.parent.skeleton        

        if bone_filters is None:
            bone_filters = {bone.name for bone in skeleton_dest.bones}
        bones_src = {bone.name for bone in skeleton_src.bones}
        bones_dest = [bone.name for bone in skeleton_dest.bones]

        # Match source anim with target anim if we have pyxenoverse filters
        if set(bones_dest) != bone_filters:
            source.set_duration(target_duration=self.frame_count)
        else:
            self.set_duration(target_duration=source.frame_count)

        new_bone_filters = bone_filters & bones_src

        # Set up paste
        if not keep_name or not self.name:
            self.name = source.name
        self.frame_float_size = source.frame_float_size
        self.frame_index_size = source.frame_index_size

        if skeleton_dest is None or skeleton_src is None:
            self.nodes = source.nodes
            return

        # Remove animation nodes
        self.nodes = list(filter(
            lambda node: skeleton_dest.bones[node.bone_index].name not in new_bone_filters, self.nodes))

        skipped_nodes = set()
        for node in source.nodes:

            index_src = node.bone_index
            if index_src >= len(skeleton_src.bones):
                continue

            name_src = skeleton_src.bones[index_src].name
            if name_src not in new_bone_filters:
                skipped_nodes.add(name_src)
                # print("pyxenoverse {} was not in filter, skipping...".format(name_src))
                continue
            try:
                index_dst = bones_dest.index(name_src)
                # print("animation for pyxenoverse {} was found in source animation, copying...".format(name_src))
                node.parent = self.parent
                node.bone_index = index_dst
                self.nodes.append(node)
            except ValueError:
                skipped_nodes.add(name_src)
                # print("pyxenoverse {} wasn't found in source animation, skipping...".format(name_src))
        return skipped_nodes

    def set_duration(self, start_frame=0, end_frame=None, target_duration=None):
        if not end_frame:
            if self.frame_count == 0:
                if target_duration:
                    self.frame_count = target_duration
                return
            end_frame = self.frame_count
        if end_frame > self.frame_count or start_frame < 0 or start_frame > end_frame:
            return
        if target_duration:
            original_duration, self.frame_count = self.frame_count, target_duration
            factor = float(target_duration) / float(original_duration)
            end_frame = round(end_frame * factor)
        else:
            self.frame_count = end_frame - start_frame
            factor = 1.0

        for node in self.nodes:
            for keyframed_animation in node.keyframed_animations:
                new_keyframes = []
                for frame in range(start_frame, end_frame):
                    new_frame = keyframed_animation.get_interpolated_frame(frame, factor)
                    if new_frame is not None:
                        new_keyframes.append(new_frame)
                if not new_keyframes:
                    new_keyframes = [Keyframe(), Keyframe()]
                if len(new_keyframes) == 1:
                    new_frame = Keyframe()
                    new_frame.paste(new_keyframes[0])
                    new_keyframes.append(new_frame)

                new_keyframes[-1].frame = (target_duration or end_frame) - 1
                keyframed_animation.keyframes = new_keyframes
                if not start_frame:
                    continue
                for keyframe in keyframed_animation.keyframes:
                    keyframe.frame -= start_frame

    def clean_nodes(self):
        bone_names = [bone.name for bone in self.parent.skeleton.bones]
        old_nodes = {node.bone_name for node in self.nodes}
        self.nodes = list(filter(lambda node: node.bone_name in bone_names, self.nodes))

        removed_nodes = old_nodes - {node.bone_name for node in self.nodes}
        for node in self.nodes:
            node.bone_index = bone_names.index(node.bone_name)
            node.clean_node_for_duration(self.frame_count)

        return removed_nodes

    def set_parent(self, ean):
        self.parent = ean

    def set_name(self, name):
        self.name = name

    def read_name(self, f):
        self.name = ''.join(list(iter(lambda: f.read(1).decode(), '\x00')))

    def write_name(self, f):
        f.write(self.name.encode())
        f.write(b'\x00')
