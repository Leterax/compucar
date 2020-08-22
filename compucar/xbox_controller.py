from inputs import get_gamepad
import time
import threading
import sys


class XboxController(threading.Thread):
    """
    Class for reading from a XboxController and keeping track of it's state.
    """

    def __init__(self, *args):
        super().__init__(*args)

        self.x = 0
        self.y = 0
        self.lz = 0
        self.rz = 0
        self.tl = 0
        self.tr = 0
        self.btn_a = 0
        self.btn_x = 0
        self.btn_y = 0
        self.btn_b = 0

        self._buttons = {
            "ABS_X",
            "ABS_Y",
            "BTN_TL",
            "BTN_TR",
            "ABS_Z",
            "ABS_RZ",
            "BTN_SOUTH",
            "BTN_NORTH",
            "BTN_EAST",
            "BTN_WEST",
        }

        self.daemon = True
        self.start()

    def run(self):
        while True:
            events = get_gamepad()
            for event in events:
                # ignore all other events
                if event.code not in self._buttons:
                    continue

                # update out internal controller state
                if event.code == "ABS_X":
                    self.x = event.state / (2 ** 15 - 1)
                elif event.code == "ABS_Y":
                    self.y = event.state / (2 ** 15 - 1)
                elif event.code == "BTN_TL":
                    self.tl = event.state
                elif event.code == "BTN_TR":
                    self.tr = event.state
                elif event.code == "ABS_Z":
                    self.lz = event.state / (2 ** 10 - 1)
                elif event.code == "ABS_RZ":
                    self.rz = event.state / (2 ** 10 - 1)
                elif event.code == "BTN_SOUTH":
                    self.btn_a = event.state
                elif event.code == "BTN_NORTH":
                    self.btn_x = event.state
                elif event.code == "BTN_WEST":
                    self.btn_y = event.state
                elif event.code == "BTN_EAST":
                    self.btn_b = event.state


if __name__ == "__main__":
    controller = XboxController()
    while True:
        sys.stdout.write("\033[2K\033[1G")
        print(
            f"x: {controller.x:.2f}, y: {controller.y:.2f}, \
            lz: {controller.lz:.2f}, rz: {controller.rz:.2f}, \
            tl: {controller.tl}, tr: {controller.tr}",
            end="\r",
        )
        time.sleep(0.025)
