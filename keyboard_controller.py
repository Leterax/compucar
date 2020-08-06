import keyboard


keys = {"w": 0, "a": 0, "s": 0, "d": 0, "t": 0, "f": 0}


def on_key(event: keyboard.KeyboardEvent):
    if event.event_type == keyboard.KEY_UP:
        keys[event.name] = 0
    elif event.event_type == keyboard.KEY_DOWN:
        keys[event.name] = 1


def hook_keys():
    for key in keys:
        keyboard.hook_key(key, on_key, True)


if __name__ == "__main__":
    hook_keys()
    while True:
        print(keys)
