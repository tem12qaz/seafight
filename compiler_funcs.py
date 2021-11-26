from math import sqrt

import numpy
from numpy import arccos, tan, pi, sin, arcsin, cos

from numba import njit


@njit(fastmath=True)
def length(x, y, z):
    return sqrt(x ** 2 + y ** 2 + z ** 2)


@njit(fastmath=True)
def norm(x, y, z):
    length_ = length(x, y, z)
    vec = (x / length_, y / length_, z / length_)
    return vec


@njit(fastmath=True)
def cos_vec(x, y, z, x2, y2, z2):
    return (x * x2 + y * y2 + z * z2) / (sqrt(x ** 2 + y ** 2 + z ** 2) * sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2))


@njit(fastmath=True)
def vector_set_len(x, y, z, length_):
    vec = norm(x, y, z)
    return vec[0] * length_, vec[1] * length_, vec[2] * length_


@njit(fastmath=True)
def vector_plus(x, y, z, x2, y2, z2):
    return x + x2, y + y2, z + z2


@njit(fastmath=True)
def flat_intersection(x, y, z, xn, yn, zn, x0, y0, z0):
    if cos_vec(-x, -y, -z, xn, yn, zn) <= 0:
        return None
    param = (xn * x0 + yn * y0 + zn * z0) / (xn * x + yn * y + zn * z)
    x = x * param
    y = y * param
    z = z * param
    vec = norm(x, y, z)
    reflection_vec = vector_rotate(*vec, *norm(xn, yn, zn), pi)
    return -reflection_vec[0], -reflection_vec[1], -reflection_vec[2], length(*vec)


@njit(fastmath=True)
def vector_rotate(x, y, z, x2, y2, z2, angle):
    rotate_matrix = numpy.array(
        [
            [cos(angle) + (1 - cos(angle)) * x2 ** 2, (1 - cos(angle)) * x2 * y2 - z2 * sin(angle),
             (1 - cos(angle)) * x2 * z2 + y2 * sin(angle)],
            [(1 - cos(angle)) * x2 * y2 + z2 * sin(angle), cos(angle) + (1 - cos(angle)) * y2 ** 2,
             (1 - cos(angle)) * y2 * z2 - x2 * sin(angle)],
            [(1 - cos(angle)) * x2 * z2 - y2 * sin(angle), (1 - cos(angle)) * y2 * z2 + x2 * sin(angle),
             cos(angle) + (1 - cos(angle)) * z2 ** 2]
        ]
    )
    vector_matrix = numpy.array([[x], [y], [z]])
    vec = numpy.dot(rotate_matrix, vector_matrix)
    return vec[0][0], vec[1][0], vec[2][0]


@njit(fastmath=True)
def sphere_intersect(center, radius, ray_origin, ray_direction):
    real_center = ray_origin - center
    b = 2 * numpy.dot(ray_direction, real_center)
    c = numpy.linalg.norm(real_center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + numpy.sqrt(delta)) / 2
        t2 = (-b - numpy.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            vec = vector_set_len(ray_direction[0], ray_direction[1], ray_direction[2], min(t1, t2))
            normal = vector_plus(*vec, real_center[0], real_center[1], real_center[2])
            reflection_vec = vector_rotate(*vec, *normal, pi)
            return (-reflection_vec[0], -reflection_vec[1], -reflection_vec[2]), vec
    return None, None


@njit(fastmath=True)
def sphere_intersection(x, y, z, x2, y2, z2, r):
    cos_ = cos_vec(x, y, z, *norm(x2, y2, z2))
    angle = arccos(cos_)
    tan_ = tan(angle)
    a = length(x2, y2, z2)
    if abs(a * tan_) < r:
        len_ = sqrt((a * tan_) ** 2 + a ** 2)
        alpla = (pi / 2 - angle)
        # print('--------------------')
        # print(a)
        # print(tan_)
        # print(cos_)
        # print(angle)
        len_2 = (r * sin(pi - alpla - arcsin((a * tan_ * sin(alpla)) / r))) / sin(alpla)
        vec = vector_set_len(x, y, z, len_ - len_2)
        normal = norm(*vector_plus(*vec, -x2, -y2, -z2))
        vec = norm(*vec)
        reflection_vec = vector_rotate(*vec, *normal, pi)
        return -reflection_vec[0], -reflection_vec[1], -reflection_vec[2], len_ - len_2
    else:
        return None
