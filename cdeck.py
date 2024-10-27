import os
import threading
import signal
import time

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Transport.Transport import TransportError

from setproctitle import setproctitle
from fractions import Fraction

from render import (
    get_key_style,
    render_key_image,
    update_key_image
)

# This is so i can use pkill to reload keymap
setproctitle("cdeck")

def refresh_keys(signum, frame):
    for key in range(deck.key_count()):
        update_key_image(deck, key, False)

def safe_exit(signum, frame):
    deck.close()
    quit()

signal.signal(signal.SIGUSR1, refresh_keys)
signal.signal(signal.SIGUSR2, safe_exit)

def key_change_callback(deck, key, pushed):
    print("Deck {} Key {} = {}".format(deck.id(), key, pushed), flush=True)

    update_key_image(deck, key, pushed)

    if pushed:
        key_style = get_key_style(deck, key, pushed)

        if key_style["name"] == "error":
            return

        os.system(key_style["action"])

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))
        print('')

        deck.set_brightness(100)

        def animate(fps):
            frame_time = Fraction(1, fps)

            next_frame = Fraction(time.monotonic())
            while deck.is_open():
                try:
                    with deck:
                        for key in range(deck.key_count()):
                            update_key_image(deck, key, False)
                except TransportError as err:
                    print("TransportError: {0}".format(err))
                    break

                next_frame += frame_time

                sleep_interval = float(next_frame) - time.monotonic()
                if sleep_interval >= 0:
                    time.sleep(sleep_interval)

        threading.Thread(target=animate, args=[60]).start()

        deck.set_key_callback(key_change_callback)

        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError as err:
                print(f"RuntimeError: {err}")
                pass
