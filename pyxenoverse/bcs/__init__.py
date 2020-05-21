from recordclass import recordclass
import struct

from pyxenoverse import write_name
from pyxenoverse.bcs.part_set import PartSet
from pyxenoverse.bcs.part_color import PartColor
from pyxenoverse.bcs.body import Body
from pyxenoverse.bcs.skeleton import Skeleton

BCS_SIGNATURE = b'#BCS'
BCSHeader = recordclass('BCSHeader', [
    'endianess_check',
    'header_size',
    'u_08',
    'num_part_sets',
    'num_part_colors',
    'num_bodies',
    'num_additional_skeletons',
    'u_14',
    'part_sets_table_offset',
    'part_colors_table_offset',
    'bodies_table_offset',
    'additional_skeleton_table_offset',
    'skeleton_table_offset',
    'u_2c',
    'f_30',
    'f_34',
    'f_38',
    'f_3c',
    'f_40',
    'f_44',
    'f_48',
])
BCS_HEADER_SIZE = 72
BCS_HEADER_BYTE_ORDER = 'HHIHHHHIIIIIIIfffffff'


class BCS:
    def __init__(self, endian='<'):
        self.header = None
        self.endian = endian
        self.filename = ''
        self.part_sets = []
        self.part_colors = []
        self.bodies = []
        self.skeletons = []

    def load(self, filename):
        with open(filename, 'rb') as f:
            if f.read(4) != BCS_SIGNATURE:
                print("Not a valid BCS file")
                return False
            self.endian = '<' if f.read(2) == b'\xFE\xFF' else '>'
            f.seek(4)
            self.read(f, self.endian)
        self.filename = filename
        return True

    def save(self, filename=None):
        if filename:
            self.filename = filename
        with open(self.filename, 'wb') as f:
            f.write(BCS_SIGNATURE)
            self.write(f, '<')

    def read(self, f, endian):
        self.header = BCSHeader(*struct.unpack(endian + BCS_HEADER_BYTE_ORDER, f.read(BCS_HEADER_SIZE)))

        # print(self.header)

        # Load part sets
        self.part_sets.clear()
        if self.header.part_sets_table_offset:
            for i in range(self.header.num_part_sets):
                f.seek(self.header.part_sets_table_offset + i * 4)
                offset = struct.unpack(endian + "I", f.read(4))[0]
                part_set = PartSet()
                if offset:
                    f.seek(offset)
                    part_set.read(f, endian)
                self.part_sets.append(part_set)

        # Load part colors
        self.part_colors.clear()
        if self.header.part_colors_table_offset:
            for i in range(self.header.num_part_colors):
                f.seek(self.header.part_colors_table_offset + i * 4)
                offset = struct.unpack(endian + "I", f.read(4))[0]
                part_color = PartColor()
                if offset:
                    f.seek(offset)
                    part_color.read(f, endian)
                self.part_colors.append(part_color)

        # Load body
        self.bodies.clear()
        if self.header.bodies_table_offset:
            for i in range(self.header.num_bodies):
                f.seek(self.header.bodies_table_offset + i * 4)
                offset = struct.unpack(endian + "I", f.read(4))[0]
                body = Body()
                if offset:
                    f.seek(offset)
                    body.read(f, endian)
                self.bodies.append(body)

        # Load skeleton
        # self.skeleton_data = None
        self.skeletons.clear()
        if self.header.skeleton_table_offset:
            f.seek(self.header.skeleton_table_offset)
            offset = struct.unpack(endian + "I", f.read(4))[0]
            skeleton = Skeleton()
            if offset:
                f.seek(offset)
                skeleton.read(f, endian)
                self.skeletons.append(skeleton)

        # Load additional skeletons
        if self.header.additional_skeleton_table_offset:
            for i in range(self.header.num_additional_skeletons):
                f.seek(self.header.additional_skeleton_table_offset)
                offset = struct.unpack(endian + "I", f.read(4))[0]
                skeleton = Skeleton()
                if offset:
                    f.seek(offset)
                    skeleton.read(f, endian)
                self.skeletons.append(skeleton)

    def write(self, f, endian):
        # Write table lengths in header
        self.header.header_size = 0x4c  # This never changes
        self.header.num_part_sets = len(self.part_sets)
        self.header.num_part_colors = len(self.part_colors)
        self.header.num_bodies = len(self.bodies)
        self.header.num_additional_skeletons = len(self.skeletons) - 1

        # Get offsets
        part_set_offset = 0x4c  # This will never change
        part_colors_offset = part_set_offset + 4 * self.header.num_part_sets
        bodies_offset = part_colors_offset + 4 * self.header.num_part_colors
        skeleton_offset = bodies_offset + 4 * self.header.num_bodies
        additional_skeletons_offset = skeleton_offset + 4

        # Set header offsets
        self.header.part_sets_table_offset = part_set_offset if self.header.num_part_sets else 0
        self.header.part_colors_table_offset = part_colors_offset if self.header.num_part_colors else 0
        self.header.bodies_table_offset = bodies_offset if self.header.num_bodies else 0
        self.header.skeleton_table_offset = skeleton_offset if self.skeletons else 0
        self.header.additional_skeleton_table_offset = additional_skeletons_offset if self.header.num_additional_skeletons else 0

        # Now that we have the header offsets, write them
        f.write(struct.pack(endian + BCS_HEADER_BYTE_ORDER, *self.header))

        # Actual data starts after the last skeleton offset
        offset_ptr = additional_skeletons_offset + 4 * self.header.num_additional_skeletons

        # All names are written at the end of the file
        names = []
        colors = []
        bone_scales = []

        # Write part sets
        for i, part_set in enumerate(self.part_sets):
            # print(f"index:{i}")
            f.seek(part_set_offset + 4 * i)
            if not part_set.parts:
                f.write(struct.pack(endian + "I", 0))
                continue
            f.write(struct.pack(endian + "I", offset_ptr))
            f.seek(offset_ptr)
            offset_ptr = part_set.write(f, names, endian)

        # Write part colors
        for i, part_color in enumerate(self.part_colors):
            f.seek(part_colors_offset + 4 * i)
            if not part_color.colors:
                f.write(struct.pack(endian + "I", 0))
                continue
            f.write(struct.pack(endian + "I", offset_ptr))
            f.seek(offset_ptr)
            offset_ptr = part_color.write(f, names, colors, endian)

        # Write floats for colors
        for colors_offset, rel_offset, color in colors:
            f.seek(colors_offset + rel_offset)
            f.write(struct.pack(endian + "I", offset_ptr - colors_offset))
            f.seek(offset_ptr)
            for c in color:
                c.write(f, endian)
            offset_ptr = f.tell()

        # Bodies
        for i, body in enumerate(self.bodies):
            f.seek(bodies_offset + 4 * i)
            if not body.bone_scales:
                f.write(struct.pack(endian + "I", 0))
                continue
            f.write(struct.pack(endian + "I", offset_ptr))
            f.seek(offset_ptr)
            offset_ptr = body.write(f, bone_scales, endian)

        # Write bone scales
        for bone_scales_offset, rel_offset, bone_scale in bone_scales:
            f.seek(bone_scales_offset + rel_offset)
            f.write(struct.pack(endian + "I", offset_ptr - bone_scales_offset))
            f.seek(offset_ptr)
            for b in bone_scale:
                b.write(f, names, endian)
            offset_ptr = f.tell()

        # Skeleton
        if self.skeletons:
            f.seek(skeleton_offset)
            f.write(struct.pack(endian + "I", offset_ptr))
            f.seek(offset_ptr)
            offset_ptr = self.skeletons[0].write(f, names, endian)

        # Additional Skeletons
        for i, skeleton in enumerate(self.skeletons[1:]):
            f.seek(additional_skeletons_offset + 4 * i)
            if not skeleton.bones:
                f.write(struct.pack(endian + "I", 0))
                continue
            f.write(struct.pack(endian + "I", offset_ptr))
            f.seek(offset_ptr)
            offset_ptr = skeleton.write(f, names, endian)

        # Write names
        for name_offset, rel_offset, name in names:
            f.seek(name_offset + rel_offset)
            f.write(struct.pack(endian + "I", offset_ptr - name_offset))
            f.seek(offset_ptr)
            write_name(f, name)
            offset_ptr = f.tell()
