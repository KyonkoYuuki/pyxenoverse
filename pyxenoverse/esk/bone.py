import struct
from recordclass import recordclass
import numpy as np

from pyxenoverse import BaseRecord


ESKBoneIndices = recordclass('ESKBoneIndices', ['parent_index', 'child_index', 'sibling_index', 'index_4'])
ESK_BONE_INDICES_SIZE = 8
ESK_BONE_INDICES_BYTE_ORDER = 'HHHH'


class Bone(BaseRecord):
    def __init__(self, index=0):
        self.name = None
        self.index = index
        self.transform_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.skinning_matrix = np.array([
            [0, 0, 0, 1],  # pos
            [0, 0, 0, 1],  # orientation quaternion x y z w
            [1, 1, 1, 0]  # scale
        ])
        super().__init__()
        self.data = ESKBoneIndices(65535, 65535, 65535, 0)

    def read_indices(self, f, endian):
        self.data = ESKBoneIndices(*struct.unpack(endian + ESK_BONE_INDICES_BYTE_ORDER, f.read(ESK_BONE_INDICES_SIZE)))
        # print("Index: {}, Parent index: {}, Child index: {}, Sibling Index: {}, Index_4: {}".format(
        #     self.index, self.parent_index, self.child_index, self.sibling_index, self.index_4))

    def write_indices(self, f, endian):
        # print("Index: {}, Parent index: {}, Child index: {}, Sibling Index: {}, Index_4: {}".format(
        #    self.index, self.parent_index, self.child_index, self.sibling_index, self.index_4))
        f.write(struct.pack(endian + ESK_BONE_INDICES_BYTE_ORDER, *self.data))

    def paste(self, source):
        self.name = source.name
        self.index = source.index
        self.data = ESKBoneIndices(source.parent_index, source.child_index, source.sibling_index, source.index_4)
        self.transform_matrix = np.copy(source.transform_matrix)
        self.skinning_matrix = np.copy(source.skinning_matrix)

    def read_skinning_matrix(self, f, endian):
        self.skinning_matrix = np.array(struct.unpack(endian + 'f' * 12, f.read(48)))
        self.skinning_matrix = np.reshape(self.skinning_matrix, (3, 4))

    def write_skinning_matrix(self, f, endian):
        f.write(struct.pack(endian + 'f' * 12, *np.reshape(self.skinning_matrix, 12)))

    def read_transform_matrix(self, f, endian):
        self.transform_matrix = np.array(struct.unpack(endian + 'f' * 16, f.read(64)))
        self.transform_matrix = np.reshape(self.transform_matrix, (4, 4))

    def write_transform_matrix(self, f, endian):
        f.write(struct.pack(endian + 'f' * 16, *np.reshape(self.transform_matrix, 16)))

    # posOrientScaleMatrix is 3x4, orient is a quaternion informations, resultTransformMatrix is 4x4
    def make_transform_4x4(self, m):
        # Ordering:
        #   1. Scale
        #   2. Rotate
        #   3. Translate
        ftx = 2 * m[1][0]
        fty = 2 * m[1][1]
        ftz = 2 * m[1][2]
        ftwx = ftx * m[1][3] # * w
        ftwy = fty * m[1][3]
        ftwz = ftz * m[1][3]
        ftxx = ftx * m[1][0] # * x
        ftxy = fty * m[1][0]
        ftxz = ftz * m[1][0]
        ftyy = fty * m[1][1] # * y
        ftyz = ftz * m[1][1]
        ftzz = ftz * m[1][2] # * z

        r = np.array([
            [1.0 - (ftyy + ftzz), ftxy - ftwz, ftxz + ftwy],
            [ftxy + ftwz, 1.0 - (ftxx + ftzz), ftyz - ftwx],
            [ftxz - ftwy, ftyz + ftwx, 1.0 - (ftxx + ftyy)]
        ])

        # Set up final matrix with scale, rotation, and translation
        return np.array([
            [m[2][0] * r[0][0], m[2][1] * r[0][1], m[2][2] * r[0][2], m[0][0]],
            [m[2][0] * r[1][0], m[2][1] * r[1][1], m[2][2] * r[1][2], m[0][1]],
            [m[2][0] * r[2][0], m[2][1] * r[2][1], m[2][2] * r[2][2], m[0][2]],
            [0, 0, 0, m[0][3]]
        ])

    def calculate_transform_matrix_from_skinning_matrix(self, bones, recursive):
        self.transform_matrix = self.make_transform_4x4(self.skinning_matrix)
        self.transform_matrix = np.transpose(self.transform_matrix)
        self.transform_matrix = np.linalg.inv(self.transform_matrix)

        if 0 <= self.parent_index < len(bones):
            parent = bones[self.parent_index]
            if recursive:
                parent.calculate_transform_matrix_from_skinning_matrix(bones, recursive)
            self.transform_matrix = np.dot(parent.transform_matrix, self.transform_matrix)
