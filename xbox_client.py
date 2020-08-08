import socket
from xbox import XboxController
import time
import struct
from utils import get_hostname_ip


def handle_input(udp_socket):
    x = int(controller.x * 100)
    y = int(controller.y * 100)
    if x < 0.1:
        x = 0
    if y < 0.1:
        y = 0

    btns = controller.top_left + 2 * controller.top_right
    udp_socket.sendto(packer.pack(x, y, btns), (HOST, PORT))


HOST = ""
PORT = 3000

controller = XboxController()
packer = struct.Struct("bbb")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        time.sleep(0.025)
        handle_input(s)
