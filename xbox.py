from inputs import get_gamepad
import time
import threading
import sys

class XboxController(threading.Thread):
    def __init__(self, *args):
        super().__init__(*args)
        self.x = 0
        self.y = 0
        self.top_left = 0
        self.top_right = 0
        self.daemon = True
        self.start()

    def run(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code not in {"ABS_X", "ABS_Y", "BTN_TL", "BTN_TR"}:
                    continue
                if event.code == "ABS_X":
                    self.x = event.state/(2**15)
                elif event.code == "ABS_Y":
                    self.y = event.state/(2**15)
                elif event.code == "BTN_TL":
                    self.top_left = event.state
                elif event.code == "BTN_TR":
                    self.top_right = event.state


if __name__ == "__main__":
    controller = XboxController()
    while True:
        sys.stdout.write('\033[2K\033[1G')
        print(f"{controller.x:.2f}, {controller.y:.2f}, {controller.top_left}, {controller.top_right}", end='\r')
        time.sleep(.025)
