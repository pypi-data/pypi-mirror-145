"""Reverse file content given as argument."""


import sys

with open(sys.argv[1]) as f:
    print(f.read()[::-1], end="")
