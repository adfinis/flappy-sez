#!/usr/bin/python3

import sys
import requests
import textwrap
import random
from datetime import datetime


FLAPPY_DATA = "https://raw.githubusercontent.com/adfinis/flappy-sez/main/flappy.txt"

MSG_CACHE_FILE = '/tmp/flappytime.txt'

HELP_TEXT = """
Get a random message and put it on display.

By default, this only puts a message on display if the current
message was set by this script. Use the `--force` parameter to change
this. This allows multiple runs during the day without disturbing other
people's usage of the display.

Here's some more options you can use:


* `--help` - show help
* `--debug` - start a debugger
* `--pretend` - don't actually do anything
* `--force` - set message even if the currently displayed message is not ours


"""


def new_message():
    lines = requests.get(FLAPPY_DATA).content.decode('utf-8').splitlines()
    return random.choice(lines).strip()


def format_message(message):
    lines = textwrap.wrap(message, 26)[:2]
    if len(lines) == 1:
        lines.append('')

    formatted_message = "%-26s%-26s" % (lines[0], lines[1])
    return formatted_message


def send_message(message):
    if '--pretend' in sys.argv:
        print("Pretending: Set message to '%s'" % message)
        return

    requests.get(
        "http://localhost:8089/set-text/%s" % message
    )
    with open(MSG_CACHE_FILE, 'w') as fh:
        fh.write(message)


def is_own_message():
    """Return true if flappy is currently showing our own message"""

    current_msg = requests.get('http://localhost:8089/get-text').content.decode('utf-8').strip()
    try:
        with open(MSG_CACHE_FILE, "r") as fh:
            return fh.read().strip() == current_msg
    except FileNotFoundError:
        # tmp file gone?
        return False


def lights_off():
    if '--pretend' in sys.argv:
        print("Pretending: lights off")
        return
    requests.get(
            "http://localhost:8089/light-off"
    )


if __name__ == '__main__':
    if '--debug' in sys.argv:
        __import__("pdb").set_trace()

    now = datetime.now().strftime('%a %d.%m.')
    message = "%s %s" % (now, new_message())
    formatted_message = format_message(message)

    if is_own_message() or '--force' in sys.argv:
        # we can overwrite: forced or own message
        send_message(formatted_message)

    if datetime.now().weekday() in (5,6):
        # on weekends, light should be turned off
        lights_off()
