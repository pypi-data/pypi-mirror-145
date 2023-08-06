import logging

from wordleparse.parser import GameParser, is_new_message_line
from wordleparse.parsers import (
    wordle_parser,
    woordle_parser,
    woordle6_parser,
    worldle_parser,
    squardle_win_parser,
    squardle_loss_parser,
    crosswordle_parser,
    primel_parser,
    letterle_parser,
    not_wordle_parser,
    nerdle_parser,
    vardle_parser,
)
from wordleparse.printers import GamePrinter, crosswordle_printer, squardle_printer
from wordleparse.util import group
from wordleparse.errors import UnparsableError

parsers = [
    wordle_parser,
    woordle_parser,
    woordle6_parser,
    worldle_parser,
    squardle_win_parser,
    squardle_loss_parser,
    crosswordle_parser,
    primel_parser,
    letterle_parser,
    not_wordle_parser,
    nerdle_parser,
    vardle_parser,
]

result_printers = [
    GamePrinter("Wordle"),
    GamePrinter("Woordle"),
    GamePrinter("Woordle6"),
    GamePrinter("Worldle"),
    GamePrinter("Primel"),
    GamePrinter("Letterle"),
    GamePrinter("Not Wordle"),
    GamePrinter("Nerdle"),
    GamePrinter("Vardle"),
    crosswordle_printer,
    squardle_printer,
]


def print_result(game, messages):
    printer = [p for p in result_printers if p.game == game]
    try:
        printer = [p for p in result_printers if p.game == game][0]
    except IndexError:
        raise ValueError(
            f"No valid printer found for game {game}. Known printers are {result_printers}"
        )
        return

    max_person_length = max([len(p) for p in {m.person for m in messages}])
    printer.print(messages, ljust=max_person_length)


def parse_messages(lines):
    messages = group(iter(lines))

    for message in messages:
        message = "".join(message)
        try:
            yield parse_message(message)
        except UnparsableError:
            continue


def parse_message(message):
    """
    Method that takes a message from a chat and returns a Message object.
    Throws UnparsableError if the message can't be parsed by any of the known
    parsers.
    """
    for parser in parsers:
        if parser.can_parse(message):
            return parser.parse(message)

    logging.info("Couldn't parse %s", message[:-1])
    raise UnparsableError()
