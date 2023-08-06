"""Truncate file given as argument by one character."""


import sys

with open(sys.argv[1]) as f:
    print(f.read()[:-1], end="")
