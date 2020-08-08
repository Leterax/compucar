import socket
import sys
import struct
import driver
import select


def get_hostname_ip():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return host_name, host_ip


_, HOST = get_hostname_ip()
PORT = 3000
buff_size = 128

last_recived = 0

unpacker = struct.Struct("bbb")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    s.setblocking(False)

    while True:
        r, _, _ = select.select([s], [], [], 1.0)
        if not r:
            stop = True
            print("lost connection")
        else:
            msg = s.recvfrom(buff_size)
            msg = msg[0]
            steering, speed, btns = unpacker.unpack(msg)
            turbo = btns & 1
            stop = (btns & 2) >> 1

        if stop:
            speed = 0
            turbo = 0
            steering = 0

        if speed > 0:
            driver.set_fast(turbo)
            driver.set_value(driver.SPEED_PIN_FORWARD, speed)
        elif speed == 0:
            driver.set_value(driver.SPEED_PIN_FORWARD, 0)
            driver.set_value(driver.SPEED_PIN_BACKWARD, 0)
        else:
            driver.set_fast(0)
            driver.set_value(driver.SPEED_PIN_BACKWARD, -speed)

        if steering > 0:
            driver.set_value(driver.STEER_PIN_RIGHT, steering)
        elif steering == 0:
            driver.set_value(driver.STEER_PIN_LEFT, 0)
            driver.set_value(driver.STEER_PIN_RIGHT, 0)
        else:
            driver.set_value(driver.STEER_PIN_LEFT, -steering)

        sys.stdout.write("\033[2K\033[1G")
        print(f"{speed:03}, {steering:03}, {turbo}, {stop}", end="\r")
