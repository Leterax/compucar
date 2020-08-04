import keyboard

pressed_keys = set()


def on_key(event: keyboard.KeyboardEvent):
    if event.event_type == keyboard.KEY_UP:
        pressed_keys.remove(event.name)
    elif event.event_type == keyboard.KEY_DOWN:
        pressed_keys.add(event.name)


def hook_keys(keys=("w", "a", "s", "d", "shift", "ctrl")):
    for key in keys:
        keyboard.hook_key(key, on_key, True)


if __name__ == "__main__":
    hook_keys()
    while True:
        print(pressed_keys)
