import re
from typing import List

from wordleparse.message import Message


DEFAULT_SCORE = r"(?P<score>[0-9X]+)/[0-9]+"


def _default_print(person: str, messages: List[Message], ljust: int) -> None:
    scores = [re.match(DEFAULT_SCORE, m.score).group("score") for m in messages]
    fails = len([s for s in scores if s == "X"])
    success = [int(s) for s in scores if s != "X"]
    print(
        f"{person.ljust(ljust)}: {len(messages)} games, "
        + f"{fails} failed attempts ({fails / len(messages):.1%}). "
        + f"Average score: {sum(success) / len(success):.2f} "
        + f"for the completed games."
    )


class GamePrinter:
    def __init__(self, game: str, print_fn=_default_print):
        self.game = game
        self.print_fn = print_fn

    def print(self, messages: List[Message], ljust: int) -> None:
        print(f"Showing stats for {self.game}")
        persons = {m.person for m in messages}
        for person in sorted(persons):
            person_messages = [m for m in messages if m.person == person]
            self.print_fn(person, person_messages, ljust)

        print("=====================\n")

    def __repr__(self):
        return f"<GamePrinter for {self.game}>"
