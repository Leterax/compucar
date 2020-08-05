import socket
import struct
import time

import keyboard_controller
from constants import *

HOST = "192.168.2.142"
PORT = 3000


packer = struct.Struct("cc")
keyboard_controller.hook_keys()


def handle_input(udp_socket):
    for key in keyboard_controller.keys:
        # turbo
        if key == "shift":
            if keyboard_controller.keys[key]:
                udp_socket.sendto(key_to_command["turbo_on"], (HOST, PORT))
            else:
                udp_socket.sendto(key_to_command["turbo_off"], (HOST, PORT))
        # rest
        elif keyboard_controller.keys[key]:
            udp_socket.sendto(key_to_command[key], (HOST, PORT))


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        time.sleep(0.025)
        handle_input(s)
