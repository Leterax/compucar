import Rpi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

# pwm frequency
FREQUENCY = 200

# pin numbers
FAST_PIN = 0
SPEED_PIN_FORWARD = 1
SPEED_PIN_BACKWARD = 2
STEER_PIN_LEFT = 3
STEER_PIN_RIGHT = 4


def set_fast(value):
    GPIO.output(FAST_PIN, value)


def set_value(pin, value):
    value = max(min(value, 100), 0)  # clamp value between 0-100
    pwm_instances[pin].ChangeDutyCycle(value)


def cleanup():
    for pwm_instance in pwm_instances.values():
        pwm_instance.stop()

    GPIO.cleanup()


def initialize_pwm():
    instances = {
        SPEED_PIN_FORWARD: GPIO.PWM(SPEED_PIN_FORWARD, FREQUENCY),
        SPEED_PIN_BACKWARD: GPIO.PWM(SPEED_PIN_BACKWARD, FREQUENCY),
        STEER_PIN_LEFT: GPIO.PWM(STEER_PIN_LEFT, FREQUENCY),
        STEER_PIN_RIGHT: GPIO.PWM(STEER_PIN_RIGHT, FREQUENCY),
    }
    # initialize all pins to duty cycle: 0
    for instance in instances.values():
        instance.start(0)
    return instances


# setting up all pins
GPIO.setup(FAST_PIN, GPIO.OUT)
GPIO.setup(SPEED_PIN_FORWARD, GPIO.OUT)
GPIO.setup(SPEED_PIN_BACKWARD, GPIO.OUT)
GPIO.setup(STEER_PIN_LEFT, GPIO.OUT)
GPIO.setup(STEER_PIN_RIGHT, GPIO.OUT)

pwm_instances = initialize_pwm()
