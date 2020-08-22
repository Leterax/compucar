key_to_command = {
    "w": b"\x01",
    "s": b"\x02",
    "a": b"\x03",
    "d": b"\x04",
    "turbo_on": b"\x05",
    "turbo_off": b"\x06",
    "f": b"\x07",
}
command_to_key = {v: k for k, v in key_to_command.items()}
