import shutil
import time

import numpy
from numba import njit, prange, jit, types, int32
from numba.core.cgutils import printf
from numba.typed.typeddict import Dict

from classes_3d import Vec3, Sphere, Camera
from compiler_funcs import norm, sphere_intersection, length, cos_vec, vector_rotate, flat_intersection
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

sp = (x+50, 0, 0, 60)
flat = (0, 0, 1, 0, 0, 1)

cam = Camera()


# @njit(fastmath=True, parallel=True)
def render(light_, camera):
    to_render = {}
    # to_render = Dict.empty(key_type=types.int64, value_type=types.char)
    while True:
        sp = (x+50-camera.x, 0-camera.y, 0, 60)
        for y in prange(columns):
            for z__ in prange(rows):
                z = rows - z__
                y_ = y - half_cols
                z_ = (rows - z - half_rows) * 2
                vec = norm(x, y_, z_)
                vec = vector_rotate(*vec, 0, 0, 1, camera.z_axis)

                try:
                    reflect_vec = sphere_intersection(*vec, *sp)
                except:
                    to_render[(y, z)] = ' '
                # reflect_vec = flat_intersection(*vec, *flat)
                if reflect_vec is not None:
                    reflect_cos = cos_vec(*reflect_vec, *light_)
                    brightness = round(16 * ((reflect_cos+1)/2))
                    symb = gradient[brightness]
                    to_render[(y, z)] = symb
                else:
                    to_render[(y, z)] = ' '

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




