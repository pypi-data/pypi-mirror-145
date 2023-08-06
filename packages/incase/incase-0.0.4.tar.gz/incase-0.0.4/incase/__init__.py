import argparse
import sys

from incase.core import Case, Caseless
from incase.extra import case_modifier, incase, planetary_defense_shield


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Convert a word from one case to another."
    )
    parser.add_argument(
        "words", type=str, nargs="+", help="The words you wish to change the case of."
    )
    parser.add_argument(
        "--case",
        dest="case",
        action="store",
        default="snake",
        help="The desired case to transform to.",
    )

    return parser.parse_args(args)


def cli():
    args = parse_args(sys.argv[1:])
    for word in args.words:
        print(incase(args.case, word))

if __name__ == "__main__":  # pragma: no cover
    cli()
