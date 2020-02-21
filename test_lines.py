#!/usr/bin/python3

import sys
import textwrap

DATE_PLACEHOLDER = "XXX DD.MM"

fails = False
with open(sys.argv[1], 'r') as fh:
    for i, line in enumerate(fh.readlines()):
        text = "%s %s" % (DATE_PLACEHOLDER, line.strip())
        lines = textwrap.wrap(text, 26)
        if len(lines) > 2:
            fails = True
            print("Line %i too long: %s" % (i, line.strip()))
        if any(len(l)>26 for l in lines):
            print("Line %i cannot be word-wrapped: %s" % (i, line.strip()))

if fails:
    sys.exit(1)
else:
    print("All lines look OK and should fit on flappy")
