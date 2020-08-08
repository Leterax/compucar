from inputs import get_gamepad
import time
import threading
import sys
import math


class XboxController(threading.Thread):
    def __init__(self, *args):
        super().__init__(*args)
        self._u = 0
        self._v = 0
        self.x = 0
        self.y = 0
        self.top_left = 0
        self.top_right = 0
        self.daemon = True
        self.start()

    def to_square(self):
        u = self._u
        v = self._v

        u2 = u ** 2
        v2 = v ** 2

        tst = 2 * math.sqrt(2)
        subtermx = 2 + u2 - v2
        subtermy = 2 - u2 + v2

        termx1 = subtermx + u * tst
        termx2 = subtermx - u * tst

        termy1 = subtermy + v * tst
        termy2 = subtermy - v * tst

        x = 0.5 * math.sqrt(termx1) - 0.5 * math.sqrt(termx2)
        y = 0.5 * math.sqrt(termy1) - 0.5 * math.sqrt(termy2)

        self.x = x
        self.y = y

    def run(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code not in {"ABS_X", "ABS_Y", "BTN_TL", "BTN_TR"}:
                    continue
                if event.code == "ABS_X":
                    self._u = event.state / (2 ** 15)
                elif event.code == "ABS_Y":
                    self._v = event.state / (2 ** 15)
                elif event.code == "BTN_TL":
                    self.top_left = event.state
                elif event.code == "BTN_TR":
                    self.top_right = event.state

            print(f"{self.x:.2f}, {self.y:.2f}")

            self.to_square()


if __name__ == "__main__":
    controller = XboxController()
    while True:
        # sys.stdout.write("\033[2K\033[1G")
        # print(f"{controller.x:.2f}, {controller.y:.2f}, {controller.top_left}, {controller.top_right}", end="\r")
        time.sleep(0.025)
