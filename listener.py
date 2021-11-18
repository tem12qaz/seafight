from pynput import keyboard


def get_listener(table):
    listener = keyboard.Listener(on_press=table.move.on_press)
    return listener


def get_online_listener(func):
    listener = keyboard.Listener(on_press=func)
    return listener
