import socket
from xbox import XboxController
import time
import struct

HOST = ""
PORT = 3000



def handle_input(udp_socket):
    x = int(controller.x * 100)
    y = int(controller.y * 100)
    btns = controller.top_left + 2*controller.top_right
    udp_socket.sendto(packer.pack(x,y,btns), (HOST, PORT))



controller = XboxController()
packer = struct.Struct('bbb')

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        time.sleep(0.025)
        handle_input(s)


