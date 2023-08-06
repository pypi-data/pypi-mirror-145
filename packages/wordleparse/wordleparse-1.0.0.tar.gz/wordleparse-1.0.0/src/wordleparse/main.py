import argparse
import logging

from wordleparse.parse import parse_messages, print_result


parser = argparse.ArgumentParser(description="Parse and aggregate Wordle chats")

parser.add_argument("filename", help="Name of file to read chat messages from")
parser.add_argument(
    "--verbose",
    "-v",
    action="count",
    default=1,
    help="Increases logging level. You can also do -vv and -vvv, etc",
)
parser.add_argument(
    "--logfile",
    "-l",
    help="Filename to log to. Overwrites on each run",
)

args = parser.parse_args()

args.verbose = 40 - (10 * args.verbose) if args.verbose > 0 else 0


if args.logfile:
    logging.basicConfig(
        filename=args.logfile, filemode="w", encoding="utf-8", level=args.verbose
    )
else:
    logging.basicConfig(level=args.verbose)


def main():
    logging.debug("Reading file %s for messages", args.filename)
    with open(args.filename) as f:
        lines = f.readlines()

    messages = list(parse_messages(lines))
    games = {m.game for m in messages}

    for game in sorted(games):
        print_result(game, [m for m in messages if m.game == game])
