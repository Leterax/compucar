import socket
import time
import atexit

import keyboard_controller
from constants import *

HOST = "192.168.2.245"
PORT = 3000


keyboard_controller.hook_keys()


def handle_input(udp_socket):
    for key in keyboard_controller.keys:
        # turbo
        if key == "t":
            if keyboard_controller.keys[key]:
                udp_socket.sendto(key_to_command["turbo_on"], (HOST, PORT))
            else:
                udp_socket.sendto(key_to_command["turbo_off"], (HOST, PORT))
        # rest
        elif keyboard_controller.keys[key]:
            udp_socket.sendto(key_to_command[key], (HOST, PORT))


def on_quit(udp_socket):
    udp_socket.sendto(key_to_command["f"], (HOST, PORT))


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    atexit.register(lambda: on_quit(s))
    while True:
        time.sleep(0.025)
        handle_input(s)
