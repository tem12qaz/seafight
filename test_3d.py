import shutil
import time
import traceback

import numpy
from numba import njit, prange, jit, types, int32
from numba.core.cgutils import printf
from numba.typed.typeddict import Dict

from classes_3d import Vec3, Sphere, Camera
from compiler_funcs import norm, sphere_intersection, length, cos_vec, vector_rotate, flat_intersection, \
    sphere_intersect
from math import pi, tan

from console_tools import clear
from listener import get_online_listener

gradient = ' .:!/r(l1Z4H9W8$@'


@njit(fastmath=True)
def print_on_x_y(x, y, symbol=' ', rows=0):
    print(f"\033[{y};{x}H{symbol}\033[{rows}A")


columns, rows = shutil.get_terminal_size((80, 20))

fov = (2/6)*pi
x = columns//(2 * tan(fov/2))

light = norm(-1, 1, 1)

half_rows = rows//2
half_cols = columns//2


flat = (0, 1, 0 , 90, 90, -70)

sp = numpy.array([x+130, 0, 0, 60])
flat = numpy.array([x+130, 0, -10061, 10000])
spheres = (sp, flat)

cam = Camera()


def reflect_sphere_(vec, dot, exclude=None):
    minimum = None
    reflect_dot_min = None
    reflect_vec_min = None
    obj = None

    for sphere in spheres:
        if exclude is not None:
            if (sphere == exclude).all():
                continue
        reflect_vec, reflect_dot = sphere_intersect(
            sphere[:3], sphere[3], numpy.array(dot), numpy.array(vec)
        )

        if reflect_vec:
            vec_len = length(*reflect_dot)
            if not minimum or vec_len < minimum:
                minimum = vec_len
                reflect_vec_min = reflect_vec
                reflect_dot_min = reflect_dot
                obj = sphere

    return reflect_vec_min, reflect_dot_min, obj


def reflect_cycle(vec, dot, sphere):
    brightness = 1
    old_vec = vec
    while brightness > 0.09:
        vec, dot, sphere = reflect_sphere_(vec, dot, sphere)
        # if brightness == 0 and (sphere == sp).any():
        #     return 0, vec
        if vec is None:
            return brightness, old_vec
        brightness *= 0.8
        old_vec = vec
    return brightness, old_vec



# @njit(fastmath=True, parallel=True)
def render(light_, camera):
    to_render = {}
    # to_render = Dict.empty(key_type=types.int64, value_type=types.char)
    while True:
        dot = numpy.array(cam.xyz)
        for y in range(columns):
            for z__ in range(rows):
                z = rows - z__
                y_ = y - half_cols
                z_ = (rows - z - half_rows) * 2
                vec = norm(x, y_, z_)
                vec = numpy.array(vector_rotate(*vec, 0, 0, 1, camera.z_axis))
                # vec = vector_rotate(*vec, 0, 1, 0, camera.y_axis)

                reflect_vec, ref_dot, obj = reflect_sphere_(vec, dot)

                if reflect_vec is not None:
                    bright_shift, reflect_vec = reflect_cycle(reflect_vec, ref_dot, obj)
                    # print(reflect_vec)
                    reflect_cos = cos_vec(*reflect_vec, *light_)
                    # brightness = round(16 * ((reflect_cos+1)/2) * bright_shift)
                    brightness = round(16 * (reflect_cos * bright_shift if reflect_cos > 0 else 0))
                    symb = gradient[brightness]
                    to_render[(y, z)] = symb
                else:
                    to_render[(y, z)] = ' '

                # try:
                #     reflect_vec = flat_intersection(*vec, *flat)
                # except:
                #     to_render[(y, z)] = ' '
                # # reflect_vec = flat_intersection(*vec, *flat)
                # if reflect_vec is not None:
                #     reflect_cos = cos_vec(*reflect_vec, *light_)
                #     brightness = round(16 * ((reflect_cos+1)/2))
                #     symb = gradient[brightness]
                #     to_render[(y, z)] = symb
                # else:
                #     to_render[(y, z)] = ' '

        to_render_str = ''
        for y_ in range(1, rows):
            for x_ in range(columns):
                to_render_str = to_render_str + to_render[x_, y_]

        print(to_render_str+f'\033[{rows}A')
        # light_ = vector_rotate(*light_, 0, 0, 1, 0.05)


if __name__ == '__main__':
    clear()
    listener_, listener_m = get_online_listener(cam.on_press, cam.on_move)
    listener_.start()
    listener_m.start()
    # time.sleep(233223)
    render(light, cam)




