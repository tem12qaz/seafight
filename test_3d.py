import shutil

from numba import njit, prange, jit
from numba.core.cgutils import printf

from classes_3d import Vec3, Sphere
from compiler_funcs import norm, sphere_intersection, length, cos_vec, vector_rotate
from math import pi, tan

from console_tools import clear

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

sp = (x+50, 0, 0, 50)


@jit(fastmath=True, parallel=True)
def render(light_):
    i = 0
    while True:
        for y in prange(columns):
            for z__ in prange(rows):
                z = rows - z__
                y_ = y - half_cols
                z_ = (rows - z - half_rows) * 2
                vec = (x, y_, z_)

                reflect_vec = sphere_intersection(*vec, *sp)
                if reflect_vec is not None:
                    reflect_cos = cos_vec(*reflect_vec, *light_)
                    brightness = round(16 * (reflect_cos if reflect_cos > 0 else 0))
                    symb = gradient[brightness]
                    print_on_x_y(y, z, symb, rows)
                else:
                    pass
                    print_on_x_y(y, z, ' ', rows)
        i+=1
        # print(i)
        light_ = vector_rotate(*light_, 0, 0, 1, 0.05)


if __name__ == '__main__':
    clear()
    render(light)




