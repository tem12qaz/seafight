import random
import shutil
import sys
import time

from console_tools import clear
from create_output import Output

test_str = '\r{u}{l} ██████╗██╗   ██╗███╗   ███╗██████╗    ██████╗  █████╗ ███╗   ███╗███████╗{r}' \
           '{l}██╔════╝╚██╗ ██╔╝████╗ ████║██╔══██╗  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝{r}' \
           '{l}╚█████╗  ╚████╔╝ ██╔████╔██║██████╦╝  ██║  ██╗ ███████║██╔████╔██║█████╗  {r}' \
           '{l} ╚═══██╗  ╚██╔╝  ██║╚██╔╝██║██╔══██╗  ██║  ╚██╗██╔══██║██║╚██╔╝██║██╔══╝  {r}' \
           '{l}██████╔╝   ██║   ██║ ╚═╝ ██║██████╦╝  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗{r}' \
           '{l}╚═════╝    ╚═╝   ╚═╝     ╚═╝╚═════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝{r}{b}'


def print_on_x_y(x, y, symbol=' ', color=''):
    print(f"{color}\033[{y};{x}H{symbol}\033[0m")


def str_to_list(string: str, cols, rows):
    str_list = []
    pos = 0
    for i in range(rows):
        str_list.append(string[pos:pos + cols].replace('\n', ''))
        pos += cols
    return str_list


def animation_2(cols, rows, str_list, fill=' ', color=''):
    center = cols//2 + 1
    for i in range(center):
        for x in range(center):
            if x == fill * rows:
                continue
            for y in range(rows):
                x_ = center - x
                if x_-i >= 0:
                    try:
                        print_on_x_y(x_ - i, y, str_list[y][x_], color=color)
                    except:
                        print_on_x_y(x_ - i, y, fill, color=color)

                x_ = x + center - 1
                try:
                    print_on_x_y(x_ + i, y, str_list[y][x_], color=color)
                except:
                    print_on_x_y(x_ + i, y, fill, color=color)


def animation(cols, rows, string=None, animation_color='', string_color='', width=25, char='░'):
    if string:
        string = format_str(string, cols, rows, ' ')
        string = str_to_list(string, cols, rows)

    to_fill = [(cols, 0)]
    max_value = cols if cols > rows else rows
    x = max_value
    y = 0
    for i in range(max_value):
        x -= 1
        y += 1
        to_fill.append((x, y))

    for i in range(cols + rows + width):
        for x, y in to_fill:
            x = x - max_value + i
            if y >= rows:
                continue
            elif x < 0:
                continue
            elif x > cols:
                if x <= cols + width:
                    try:
                        print_on_x_y(x - width, y, ' ' if not string else string[y][x - width], string_color)
                    except:
                        print_on_x_y(x - width, y, ' ')
                continue

            print_on_x_y(x, y, char, animation_color)
            if x >= width:
                try:
                    print_on_x_y(x - width, y, ' ' if not string else string[y][x - width], string_color)
                except:
                    print_on_x_y(x - width, y, ' ')
        if i % 15 == 0:
            time.sleep(0.000001)

    return string


def format_str(string: str, cols: int, rows: int, fill=' '):
    str_rows = string.count(r'{l}')
    str_cols = len(string[string.find(r'{l}') + 3:string.find(r'{r}')])

    row = fill * cols

    if str_cols > cols or str_rows > rows:
        clear()
        return f'\r\033[91mPlease enlarge the terminal size\033[0m'

    left_right_count = cols - str_cols
    right = left_right_count // 2

    left = (left_right_count - right) * fill
    right = right * fill

    up_bottom_count = rows - str_rows
    up = up_bottom_count // 2

    bottom = (up_bottom_count - up - 1) * row + f'\033[{rows}A'
    up = up * row

    string = string.format(l=left, r=right, u=up, b=bottom)
    return string


def main():
    clear()
    colors = ['p', 'b', 'c', 'g', 'y', 'r']
    while True:
        color = random.choice(colors)
        columns, rows = shutil.get_terminal_size((80, 20))
        time.sleep(1)
        str_list = animation(columns, rows, test_str, getattr(Output, color), getattr(Output, color), width=25)
        time.sleep(1)
        animation_2(columns, rows, str_list, color=getattr(Output, color))
        time.sleep(1)
        # print(getattr(Output, color) + format_str(test_str, columns, rows) + '\033[0m')
        # time.sleep(3333)


main()
