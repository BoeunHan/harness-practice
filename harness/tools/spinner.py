import itertools
import time


def spinner(stop_event):
    for dots in itertools.cycle(["⚙️", "⚙️🔨", "⚙️🔨🔥"]):
        if stop_event.is_set():
            break
        print(f"\rLoading {dots}", end="", flush=True)
        time.sleep(0.3)
    print("\r", end="")
