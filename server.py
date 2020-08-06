import socket
import driver
from constants import *


HOST = "192.168.2.245"
PORT = 3000
buff_size = 128

STEP_VALUE = 5

speed = 0
steering = 0
turbo = 0

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))

    while True:
        msg = s.recvfrom(buff_size)
        command = command_to_key[msg[0]]

        if command == "w":
            speed += STEP_VALUE
        elif command == "s":
            speed -= STEP_VALUE
        if command == "a":
            steering -= STEP_VALUE
        elif command == "d":
            steering += STEP_VALUE

        if command == "turbo_on":
            turbo = 1
        elif command == "turbo_off":
            turbo = 0

        if command == "f":
            speed = 0
            steering = 0
            turbo = 0

        speed = max(min(100, speed), -100)
        steering = max(min(100, steering), -100)

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

        print(f"{speed}, {steering}, {bool(turbo)}                          ", end="\r")
