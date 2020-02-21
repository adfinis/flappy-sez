#!/usr/bin/python3

import sys
import string
import textwrap

DATE_PLACEHOLDER = "XXX DD.MM"
ALLOWED_CHARACTERS = set(string.ascii_letters + string.digits + " " + "." + "/" + "-")

fails = False
with open(sys.argv[1], "r") as fh:
    for i, line in enumerate(fh.read().splitlines()):
        # Check for invalid characters
        if not set(line).issubset(ALLOWED_CHARACTERS):
            fails = True
            print("Line %i contains invalid characters: %s" % (i + 1, line))

        # Check for wordwrapping
        text = "%s %s" % (DATE_PLACEHOLDER, line)
        lines = textwrap.wrap(text, 26)
        if len(lines) > 2:
            fails = True
            print("Line %i too long: %s" % (i + 1, line))
        if any(len(l) > 26 for l in lines):
            print("Line %i cannot be word-wrapped: %s" % (i + 1, line))

if fails:
    sys.exit(1)
else:
    print("All lines look OK and should fit on flappy")
