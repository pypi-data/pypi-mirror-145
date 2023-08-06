import re
from typing import List

from wordleparse.printers.printers import GamePrinter
from wordleparse.message import Message


def print_fn(person: str, messages: List[Message], ljust: int) -> None:
    scores = [
        re.match(r"([0-9]+)?(?:m )?([0-9]+)s", m.score).groups() for m in messages
    ]
    seconds = sum(
        [int(x[-1]) + 60 * int(x[0]) if len(x) > 1 else int(x[-1]) for x in scores]
    )
    print(
        f"{person.ljust(ljust)}: {len(messages)} games, average time of "
        + f"{seconds / len(messages):.0f}s"
    )


crosswordle_printer = GamePrinter("Crosswordle", print_fn)
