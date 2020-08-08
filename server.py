import socket
import sys
import struct
import select


# if we are on the compucar this will succeed
# if we are not, we enter debug mode
try:
    import driver
    DEBUG = False
except ImportError:
    DEBUG = True

HOST = "127.0.0.1" if "--local" in sys.argv else sys.argv[1]
PORT = 3000
buff_size = 128

last_recived = 0

unpacker = struct.Struct("bbb")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    s.setblocking(False)

    print(f"Bound to {HOST}:{PORT} and{' ' if DEBUG else ' not '}running in debug mode")

    while True:
        r, _, _ = select.select([s], [], [], 1.0)
        if not r:
            stop = True
            sys.stdout.write("\033[2K\033[1G")
            print("lost connection", end='\r')
            continue
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

        if DEBUG:
            sys.stdout.write("\033[2K\033[1G")
            print(f"DEBUGING: {speed:03}, {steering:03}, {turbo}, {stop}", end="\r")
            continue

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
