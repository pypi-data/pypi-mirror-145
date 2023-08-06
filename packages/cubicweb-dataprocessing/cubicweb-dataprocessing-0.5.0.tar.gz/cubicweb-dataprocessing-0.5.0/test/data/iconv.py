"""Convert a text from one encoding to another"""
import argparse
import sys

import codecs


def iconv(infile, outfile, from_encoding="latin1", to_encoding="utf-8"):
    for line in infile:
        outfile.write(line.decode(from_encoding).encode(to_encoding))


def parse():
    parser = argparse.ArgumentParser(description="Encoding converter.")
    parser.add_argument("fpath", type=str)
    parser.add_argument(
        "--from",
        type=str,
        default="latin1",
        dest="from_",
        metavar="FROM",
        help="encoding to convert from",
    )
    parser.add_argument(
        "--to", type=str, default="utf-8", help="encoding to convert to"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse()
    with codecs.open(args.fpath, mode="rb") as f:
        iconv(f, sys.stdout, from_encoding=args.from_, to_encoding=args.to)
