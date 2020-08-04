from compucar import keyboard_controller, driver


class Car:
    speed_forward = 0
    speed_backward = 0
    steering_left = 0
    steering_right = 0


def handle_input():
    keys = keyboard_controller.pressed_keys
    if "shift" in keys:
        Car.speed_forward += 1
        Car.speed_forward = max(min(Car.speed_forward, 100), 0)
        driver.set_value(driver.SPEED_PIN_FORWARD, Car.speed_forward)

    if "ctrl" in keys:
        Car.speed_forward -= 1
        Car.speed_forward = max(min(Car.speed_forward, 100), 0)
        driver.set_value(driver.SPEED_PIN_FORWARD, Car.speed_forward)


if __name__ == "__main__":
    keyboard_controller.hook_keys()

    try:
        while True:
            handle_input()
    except Exception as e:
        driver.cleanup()
        raise e
