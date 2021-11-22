from pynput import keyboard, mouse


def get_listener(table):
    listener = keyboard.Listener(on_press=table.move.on_press)
    return listener


def get_online_listener(func, func_m):
    listener = keyboard.Listener(on_press=func)
    listener_m = mouse.Listener(on_move=func_m)
    return listener, listener_m
