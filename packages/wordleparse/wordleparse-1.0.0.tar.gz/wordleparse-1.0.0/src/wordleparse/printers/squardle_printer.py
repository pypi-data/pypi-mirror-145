from typing import List

from wordleparse.printers.printers import GamePrinter
from wordleparse.message import Message


def print_fn(person: str, messages: List[Message], ljust: int) -> None:
    fails = [m for m in messages if "/" in m.score]
    success = [int(m.score) for m in messages if m not in fails]
    print(
        f"{person.ljust(ljust)}: {len(messages)} games, {len(fails)} failed attempts. "
        + f"Average guesses left: {sum(success) / len(success):.1f} "
        + "for the completed games."
    )


squardle_printer = GamePrinter("Squardle", print_fn)
