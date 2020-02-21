#!/usr/bin/python3

import requests
import textwrap
import random
from datetime import datetime

FLAPPY_DATA="https://raw.githubusercontent.com/adfinis-sygroup/flappy-sez/master/flappy.txt"

now = datetime.now().strftime('%a %d.%m')

lines = requests.get(FLAPPY_DATA).content.decode('utf-8').splitlines()

our_line = random.choice(lines)

full_line = "%s %s" % (now, our_line)

lines = textwrap.wrap(full_line, 26)[:2]
if len(lines) == 1:
    lines.append('')

formatted_message = "%-26s%-26s" % (lines[0], lines[1])
print("'%s'" % formatted_message)

requests.get(
    "http://flappy.syfinis.ch:8089/set-text/%s" % formatted_message
)
if datetime.now().weekday() in (5,6):
    requests.get(
        "http://flappy.syfinis.ch/api/v1/light-off"
    )
