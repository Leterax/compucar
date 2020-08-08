import socket
from xbox_controller import XboxController
import time
import struct


def handle_input(udp_socket):
    x = int(controller.x * 100)
    y = int((controller.rz - controller.lz) * 100)
    if abs(x) < 6:
        x = 0
    if abs(y) < 2:
        y = 0

    btns = controller.tl + 2 * controller.btn_a
    udp_socket.sendto(packer.pack(x, y, btns), (HOST, PORT))


HOST = "127.0.0.1"
PORT = 3000

controller = XboxController()
packer = struct.Struct("bbb")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        time.sleep(0.025)
        handle_input(s)
