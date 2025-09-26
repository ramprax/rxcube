from abc import ABC, abstractmethod

try:
    from typing import Self
except ImportError:
    Self = None

import itertools

FACES = 'ULFRBD'
OPPOSITE_FACES = dict([(FACES[_i], _f) for _i, _f in enumerate('DRBLFU')])

STATES = 'ULFRBD'

COLOUR_MAP_OLD = {
    'D': 'w', 
    'U': 'y',
    'F': 'g',
    'L': 'r',
    'R': 'o',
    'B': 'b',
}

COLOUR_MAP = {
    'D': 'y', 
    'U': 'w',
    'F': 'g',
    'L': 'o',
    'R': 'r',
    'B': 'b',
}


class Cube(ABC):
    def __init__(self, size, u, l, f, r, b, d):
        self._size = size
        self._u = u[:]
        self._l = l[:]
        self._f = f[:]
        self._r = r[:]
        self._b = b[:]
        self._d = d[:]

    @property
    def size(self):
        return self._size

    @classmethod
    @abstractmethod
    def make_cube(cls) -> Self:
        raise NotImplementedError()

    def make_move(self, move_str):
        match move_str.upper():
            case "R":
                # print('Making R move')
                return self.move_R()
            case "R'":
                return self.move_r()
            case "R2":
                return self.move_R().move_R()
            case "U":
                return self.move_U()
            case "U'":
                return self.move_u()
            case "U2":
                return self.move_U().move_U()
            case "F":
                return self.move_F()
            case "F'":
                return self.move_f()
            case "F2":
                return self.move_F().move_F()
            case "L":
                return self.move_L()
            case "L'":
                return self.move_l()
            case "L2":
                return self.move_L().move_L()
            case "D":
                return self.move_D()
            case "D'":
                return self.move_d()
            case "D2":
                return self.move_D().move_D()
            case "B":
                return self.move_B()
            case "B'":
                return self.move_b()
            case "B2":
                return self.move_B().move_B()
            case "X":
                return self.rotate_X()
            case "X'":
                return self.rotate_x()
            case "X2":
                return self.rotate_X().rotate_X()
            case "Y":
                return self.rotate_Y()
            case "Y'":
                return self.rotate_y()
            case "Y2":
                return self.rotate_Y().rotate_Y()
            case "Z":
                return self.rotate_Z()
            case "Z'":
                return self.rotate_z()
            case "Z2":
                return self.rotate_Z().rotate_Z()
        raise NotImplementedError(move_str)

    def non_rotational_moves(self):
        move_suffixes = ("", "'", "2")
        return [f'{f}{m}' for f, m in itertools.product(FACES, move_suffixes)]

    def whole_cube_rotation_moves(self):
        axes = 'XYZ'
        move_suffixes = ("", "'", "2")
        return [f'{v}{m}' for v, m in itertools.product(axes, move_suffixes)]

    def _unpack_faces(self):
        return self._u[:], self._l[:], self._f[:], self._r[:], self._b[:], self._d[:]

    @staticmethod
    @abstractmethod
    def _turn_face_anticlockwise(face):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def _turn_face_clockwise(face):
        raise NotImplementedError()
    
    @abstractmethod
    def move_U(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_u(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_R(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_r(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_F(self) -> Self:
        ...

    @abstractmethod
    def move_f(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_L(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_l(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_B(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_b(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_D(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def move_d(self) -> Self:
        raise NotImplementedError()

    def rotate_X(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_f = u[:]
        new_d = f[:]

        new_b = self._turn_face_clockwise(self._turn_face_clockwise(d[:]))

        new_u = self._turn_face_clockwise(self._turn_face_clockwise(b[:]))

        new_r = r[:]
        new_r = self._turn_face_anticlockwise(new_r)

        new_l = l[:]
        new_l = self._turn_face_clockwise(new_l)

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def rotate_x(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_u = f[:]
        new_f = d[:]

        new_d = self._turn_face_clockwise(self._turn_face_clockwise(b[:]))

        new_b = self._turn_face_clockwise(self._turn_face_clockwise(u[:]))

        new_r = r[:]
        new_r = self._turn_face_clockwise(new_r)

        new_l = l[:]
        new_l = self._turn_face_anticlockwise(new_l)

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def rotate_Y(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_f = l[:]
        new_r = f[:]
        new_b = r[:]
        new_l = b[:]

        new_u = u[:]
        new_u = self._turn_face_anticlockwise(new_u)

        new_d = d[:]
        new_d = self._turn_face_clockwise(new_d)

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def rotate_y(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_l = f[:]
        new_f = r[:]
        new_r = b[:]
        new_b = l[:]

        new_u = u[:]
        new_u = self._turn_face_clockwise(new_u)

        new_d = d[:]
        new_d = self._turn_face_anticlockwise(new_d)

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def rotate_Z(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_l = u[:]
        new_l = self._turn_face_anticlockwise(new_l)

        new_d = l[:]
        new_d = self._turn_face_anticlockwise(new_d)

        new_r = d[:]
        new_r = self._turn_face_anticlockwise(new_r)

        new_u = r[:]
        new_u = self._turn_face_anticlockwise(new_u)

        new_f = f[:]
        new_f = self._turn_face_anticlockwise(new_f)

        new_b = b[:]
        new_b = self._turn_face_clockwise(new_b)

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def rotate_z(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_u = l[:]
        new_u = self._turn_face_clockwise(new_u)

        new_l = d[:]
        new_l = self._turn_face_clockwise(new_l)

        new_d = r[:]
        new_d = self._turn_face_clockwise(new_d)

        new_r = u[:]
        new_r = self._turn_face_clockwise(new_r)

        new_f = f[:]
        new_f = self._turn_face_clockwise(new_f)

        new_b = b[:]
        new_b = self._turn_face_anticlockwise(new_b)

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    @abstractmethod
    def face_centre_index(self):
        raise NotImplementedError()

    def correct_face_orientation(self):
        u, l, f, r, b, d = self._unpack_faces()

        fci = self.face_centre_index()

        # Where is U?
        if u[fci] == 'U':
            ...
        else:
            if l[fci] == 'U':
                u, l, f, r, b, d = self.rotate_z()._unpack_faces()
            if f[fci] == 'U':
                u, l, f, r, b, d = self.rotate_x()._unpack_faces()
            if r[fci] == 'U':
                u, l, f, r, b, d = self.rotate_Z()._unpack_faces()
            if b[fci] == 'U':
                u, l, f, r, b, d = self.rotate_X()._unpack_faces()
            if d[fci] == 'U':
                u, l, f, r, b, d = self.rotate_X().rotate_X()._unpack_faces()

        while l[fci] != 'L':
            u, l, f, r, b, d = self.rotate_Y()._unpack_faces()

        new_cube = self.__class__(u, l, f, r, b, d)

        return new_cube

    def is_solved(self):
        print(self.to_cube_string())

        u, l, f, r, b, d = self._unpack_faces()
        for face in (u, l, f, r, b, d):
            if len(set(face)) > 1:
                return False

        cbstr = self.correct_face_orientation().to_cube_string()
        print(cbstr)
        new_cbstr = self.make_cube().to_cube_string()
        print(new_cbstr)
        return cbstr == new_cbstr

    def to_cube_string(self):
        flattened = sum(self._unpack_faces(), [])
        cube_str = ''.join(flattened)
        return cube_str

    @classmethod
    @abstractmethod
    def from_cube_string(cls, cube_string):
        raise NotImplementedError()

    def print_cube(self):
        sz = self.size
        fc_size = sz * sz
        u_face, l_face, f_face, r_face, b_face, d_face = self._unpack_faces()

        u_face_rows = [u_face[i:i + sz] for i in range(0, fc_size, sz)]
        lfrb_rows = [
            l_face[i:i + sz] + f_face[i:i + sz] + r_face[i:i + sz] + b_face[i:i + sz]
            for i in range(0, fc_size, sz)
        ]
        d_face_rows = [d_face[i:i + sz] for i in range(0, fc_size, sz)]

        columns_per_cell = 3
        columns_per_row = columns_per_cell * sz
        indent_spaces = ' ' * columns_per_row
        cell_space_padding = ' ' * int((columns_per_cell - 1) / 2)

        u_face_str = '\n'.join([indent_spaces + (
            ''.join([
                        f'{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}'
                        for cell in row])) for row
                                in u_face_rows])

        lfrb_rows_str = '\n'.join(
            [''.join([
                         f'{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}'
                         for cell in lfrb_row]) for
             lfrb_row in lfrb_rows])

        d_face_str = '\n'.join([indent_spaces + (
            ''.join([
                        f'{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}'
                        for cell in row])) for row
                                in d_face_rows])

        cube_display_str = '\n'.join([u_face_str, lfrb_rows_str, d_face_str])

        print(cube_display_str)


class Cube_3x3x3(Cube):
    SIZE = 3

    def __init__(self, u, l, f, r, b, d):
        super().__init__(self.SIZE, u, l, f, r, b, d)

    @classmethod
    def from_cube_string(cls, cube_string):
        assert len(cube_string) == 54
        face_strs = [cube_string[i:i + 9] for i in range(0, 54, 9)]
        cube_array = [[cell for cell in f] for f in face_strs]
        return cls(*cube_array)

    # @classmethod
    # def from_cube_array(cls, cube_array):
    #     ...

    @staticmethod
    def _turn_face_clockwise(face):
        new_face = face[:]
        new_face[0] = face[6]
        new_face[1] = face[3]
        new_face[2] = face[0]
        new_face[3] = face[7]
        new_face[5] = face[1]
        new_face[6] = face[8]
        new_face[7] = face[5]
        new_face[8] = face[2]

        return new_face

    @staticmethod
    def _turn_face_anticlockwise(face):
        new_face = face[:]
        new_face[0] = face[2]
        new_face[1] = face[5]
        new_face[2] = face[8]
        new_face[3] = face[1]
        new_face[5] = face[7]
        new_face[6] = face[0]
        new_face[7] = face[3]
        new_face[8] = face[6]

        return new_face

    def move_U(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_u = self._turn_face_clockwise(new_u)

        new_l[0] = f[0]
        new_l[1] = f[1]
        new_l[2] = f[2]

        new_f[0] = r[0]
        new_f[1] = r[1]
        new_f[2] = r[2]

        new_r[0] = b[0]
        new_r[1] = b[1]
        new_r[2] = b[2]

        new_b[0] = l[0]
        new_b[1] = l[1]
        new_b[2] = l[2]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_u(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_u = self._turn_face_anticlockwise(new_u)

        new_f[0] = l[0]
        new_f[1] = l[1]
        new_f[2] = l[2]

        new_r[0] = f[0]
        new_r[1] = f[1]
        new_r[2] = f[2]

        new_b[0] = r[0]
        new_b[1] = r[1]
        new_b[2] = r[2]

        new_l[0] = b[0]
        new_l[1] = b[1]
        new_l[2] = b[2]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_R(self):
        # print('Performing R move')
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_r = self._turn_face_clockwise(new_r)

        new_f[2] = d[2]
        new_f[5] = d[5]
        new_f[8] = d[8]

        new_u[2] = f[2]
        new_u[5] = f[5]
        new_u[8] = f[8]

        new_b[0] = u[8]
        new_b[3] = u[5]
        new_b[6] = u[2]

        new_d[2] = b[6]
        new_d[5] = b[3]
        new_d[8] = b[0]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_r(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_r = self._turn_face_anticlockwise(new_r)

        new_d[2] = f[2]
        new_d[5] = f[5]
        new_d[8] = f[8]

        new_f[2] = u[2]
        new_f[5] = u[5]
        new_f[8] = u[8]

        new_u[8] = b[0]
        new_u[5] = b[3]
        new_u[2] = b[6]

        new_b[6] = d[2]
        new_b[3] = d[5]
        new_b[0] = d[8]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_F(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_f = self._turn_face_clockwise(new_f)

        new_l[2] = d[0]
        new_l[5] = d[1]
        new_l[8] = d[2]

        new_u[6] = l[8]
        new_u[7] = l[5]
        new_u[8] = l[2]

        new_r[0] = u[6]
        new_r[3] = u[7]
        new_r[6] = u[8]

        new_d[0] = r[6]
        new_d[1] = r[3]
        new_d[2] = r[0]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_f(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_f = self._turn_face_anticlockwise(new_f)

        new_d[0] = l[2]
        new_d[1] = l[5]
        new_d[2] = l[8]

        new_l[8] = u[6]
        new_l[5] = u[7]
        new_l[2] = u[8]

        new_u[6] = r[0]
        new_u[7] = r[3]
        new_u[8] = r[6]

        new_r[6] = d[0]
        new_r[3] = d[1]
        new_r[0] = d[2]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_L(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_l = self._turn_face_clockwise(new_l)

        new_f[0] = u[0]
        new_f[3] = u[3]
        new_f[6] = u[6]

        new_u[0] = b[8]
        new_u[3] = b[5]
        new_u[6] = b[2]

        new_b[2] = d[6]
        new_b[5] = d[3]
        new_b[8] = d[0]

        new_d[0] = f[0]
        new_d[3] = f[3]
        new_d[6] = f[6]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_l(self):
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_l = self._turn_face_anticlockwise(new_l)

        new_u[0] = f[0]
        new_u[3] = f[3]
        new_u[6] = f[6]

        new_b[8] = u[0]
        new_b[5] = u[3]
        new_b[2] = u[6]

        new_d[6] = b[2]
        new_d[3] = b[5]
        new_d[0] = b[8]

        new_f[0] = d[0]
        new_f[3] = d[3]
        new_f[6] = d[6]

        new_cube = Cube_3x3x3(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_B(self):
        return self.rotate_X().move_U().rotate_x()  #  self.rotate_x(self.move_U(self.rotate_X(cube)))

    def move_b(self):
        return self.rotate_X().move_u().rotate_x()  #   rotate_x(move_u(rotate_X(cube)))

    def move_D(self):
        return self.rotate_x().move_F().rotate_X() # rotate_X(move_F(rotate_x(cube)))

    def move_d(self):
        return self.rotate_x().move_f().rotate_X()  # rotate_X(move_f(rotate_x(cube)))

    def face_centre_index(self):
        return 4

    @classmethod
    def make_cube(cls):
        """
             U
           L F R B
             D
             
           U L F R B D
        """
        cube = [[STATES[i]]*9 for i, f in enumerate(FACES)]
        return cls(*cube)


class Cube_2x2x2(Cube):
    SIZE = 2

    def __init__(self, u, l, f, r, b, d):
        super().__init__(self.SIZE, u, l, f, r, b, d)

    @classmethod
    def make_cube(cls):
        """
             U
           L F R B
             D

           U L F R B D
        """
        cube = [[STATES[i]] * 4 for i, f in enumerate(FACES)]
        return cls(*cube)

    @classmethod
    def from_cube_string(cls, cube_string):
        assert len(cube_string) == 24
        face_strs = [cube_string[i:i + 4] for i in range(0, 24, 4)]
        cube_array = [[cell for cell in f] for f in face_strs]
        return cls(*cube_array)

    @staticmethod
    def _turn_face_clockwise(face):
        new_face = face[:]
        new_face[0] = face[2]
        new_face[1] = face[0]
        new_face[2] = face[3]
        new_face[3] = face[1]

        return new_face
    @staticmethod
    def _turn_face_anticlockwise(face):
        new_face = face[:]
        new_face[0] = face[1]
        new_face[1] = face[3]
        new_face[2] = face[0]
        new_face[3] = face[2]

        return new_face

    def move_U(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_u = self._turn_face_clockwise(new_u)

        new_l[0] = f[0]
        new_l[1] = f[1]

        new_f[0] = r[0]
        new_f[1] = r[1]

        new_r[0] = b[0]
        new_r[1] = b[1]

        new_b[0] = l[0]
        new_b[1] = l[1]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_u(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_u = self._turn_face_anticlockwise(new_u)

        new_f[0] = l[0]
        new_f[1] = l[1]

        new_r[0] = f[0]
        new_r[1] = f[1]

        new_b[0] = r[0]
        new_b[1] = r[1]

        new_l[0] = b[0]
        new_l[1] = b[1]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_R(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_r = self._turn_face_clockwise(new_r)

        new_f[1] = d[1]
        new_f[3] = d[3]

        new_u[1] = f[1]
        new_u[3] = f[3]

        new_b[0] = u[3]
        new_b[2] = u[1]

        new_d[1] = b[2]
        new_d[3] = b[0]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_r(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_r = self._turn_face_anticlockwise(new_r)

        new_d[1] = f[1]
        new_d[3] = f[3]

        new_f[1] = u[1]
        new_f[3] = u[3]

        new_u[3] = b[0]
        new_u[1] = b[2]

        new_b[2] = d[1]
        new_b[0] = d[3]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_F(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_f = self._turn_face_clockwise(new_f)

        new_l[1] = d[0]
        new_l[3] = d[1]

        new_u[2] = l[3]
        new_u[3] = l[1]

        new_r[0] = u[2]
        new_r[2] = u[3]

        new_d[0] = r[2]
        new_d[1] = r[0]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_f(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_f = self._turn_face_anticlockwise(new_f)

        new_d[0] = l[1]
        new_d[1] = l[3]

        new_l[3] = u[2]
        new_l[1] = u[3]

        new_u[2] = r[0]
        new_u[3] = r[2]

        new_r[2] = d[0]
        new_r[0] = d[1]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_L(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_l = self._turn_face_clockwise(new_l)

        new_f[0] = u[0]
        new_f[2] = u[2]

        new_u[0] = b[3]
        new_u[2] = b[1]

        new_b[1] = d[2]
        new_b[3] = d[0]

        new_d[0] = f[0]
        new_d[2] = f[2]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_l(self) -> Self:
        u, l, f, r, b, d = self._unpack_faces()

        new_u = u[:]
        new_l = l[:]
        new_f = f[:]
        new_r = r[:]
        new_b = b[:]
        new_d = d[:]

        new_l = self._turn_face_anticlockwise(new_l)

        new_u[0] = f[0]
        new_u[2] = f[2]

        new_b[3] = u[0]
        new_b[1] = u[2]

        new_d[2] = b[1]
        new_d[0] = b[3]

        new_f[0] = d[0]
        new_f[2] = d[2]

        new_cube = self.__class__(new_u, new_l, new_f, new_r, new_b, new_d)

        return new_cube

    def move_B(self):
        return self.rotate_X().move_U().rotate_x()  #  self.rotate_x(self.move_U(self.rotate_X(cube)))

    def move_b(self):
        return self.rotate_X().move_u().rotate_x()  #   rotate_x(move_u(rotate_X(cube)))

    def move_D(self):
        return self.rotate_x().move_F().rotate_X() # rotate_X(move_F(rotate_x(cube)))

    def move_d(self):
        return self.rotate_x().move_f().rotate_X()  # rotate_X(move_f(rotate_x(cube)))

    def face_centre_index(self):
        return 0


def from_cube_string(cube_string):
    match len(cube_string):
        case 54:
            return Cube_3x3x3.from_cube_string(cube_string)
        case 24:
            return Cube_2x2x2.from_cube_string(cube_string)
    raise NotImplementedError(cube_string)


def make_cube(size):
    match size:
        case 3:
            return Cube_3x3x3.make_cube()
        case 2:
            return Cube_2x2x2.make_cube()
    raise NotImplementedError(size)



