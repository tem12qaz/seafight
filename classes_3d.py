import time

import numpy as np
from math import sqrt

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