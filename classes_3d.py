import time

import numpy as np
from math import sqrt, cos, sin

from numba import int32, njit, float64
from numba.experimental import jitclass

from compiler_funcs import length, norm

spec_vec3 = [
    ('x', float64),
    ('y', float64),
    ('z', float64),
]

spec_sphere = [
    ('x', float64),
    ('y', float64),
    ('z', float64),
    ('r', float64),
]


@jitclass(spec_sphere)
class Sphere:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    @property
    def xyzr(self):
        return self.x, self.y, self.z, self.r

@jitclass(spec_vec3)
class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def xyz(self):
        return self.x, self.y, self.z

    def length(self):
        return length(self.x, self.y, self.z)

    def normalize(self):
        length = self.length()
        if length == 0:
            return self
        return Vec3(*norm(self.x, self.y, self.z, length))


class Camera:
    def __init__(self):
        self.start = True
        self.z_axis = 0
        self.z_axis_old = 0
        self.y_axis = 0
        self.y_axis_old = 0

        self.x = 0
        self.z = 0
        self.y = 0
        self.p = 0
        self.speed = 5
        self.s = 0

    @property
    def xyz(self):
        return self.x, self.y, self.z

    def on_move(self, x, y):
        if self.start:
            self.z_axis_old = (x/4)/57.29
            self.y_axis_old = (y/4)/57.29
            self.start = False

        self.z_axis = (x/4)/57.29 - self.z_axis_old
        self.y_axis = (y/4)/57.29 - self.y_axis_old

    def on_press(self, key):
        key_str = str(key)
        if key_str == 'Key.right':
            self.p += 10

        elif key_str == 'Key.left':
            self.p -= 10

        elif key_str == 'Key.up':
            self.speed += 1

        elif key_str == 'Key.down':
            self.speed -= 1

        elif key_str in ("'x'", "'X'"):
            self.s += 10

        elif key_str in ("'z'", "'Z'"):
            self.s -= 10

        elif key_str in ("'w'", "'W'"):
            self.x += cos(self.z_axis) * self.speed
            self.y += sin(self.z_axis) * self.speed

        elif key_str in ("'s'", "'S'"):
            self.x -= cos(self.z_axis) * self.speed
            self.y -= sin(self.z_axis) * self.speed

        elif key_str in ("'a'", "'A'"):
            self.x += sin(self.z_axis) * self.speed
            self.y -= cos(self.z_axis) * self.speed

        elif key_str in ("'d'", "'D'"):
            self.x -= sin(self.z_axis) * self.speed
            self.y += cos(self.z_axis) * self.speed



@njit(fastmath=True)
def main():
    for i in range(1, 10000000):
        # vec = np.array((i, i, i))
        # length = vec3_length_compiler(vec[0], vec[1], vec[2])
        # vec3_normalize_compiler(vec[0], vec[1], vec[2], length)

        vec = Vec3(i, i, i)
        vec.normalize()
        # length = vec3_length_compiler(*vec.xyz)
        # vec3_normalize_compiler(*vec.xyz, length)



if __name__ == '__main__':
    now = time.time()
    main()
    print(time.time() - now)