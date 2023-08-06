import re

from wordleparse.message import Message
from wordleparse.errors import UnparsableError


BEGIN_RE = r"([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{2}:[0-9]{2}) - ([\s\S]+)"
PERSON_RE = r"([\w <]+): ([\s\S]+)"
SCORE_RE = r"([0-9X]+)/[0-9]+"


class GameParser:
    def __init__(
        self,
        game,
        game_regex,
        begin_regex=BEGIN_RE,
        person_regex=PERSON_RE,
        score_regex=SCORE_RE,
    ):
        self.game = game
        self.game_regex = game_regex
        self.begin_regex = begin_regex
        self.person_regex = person_regex
        self.score_regex = score_regex

    def can_parse(self, message: str) -> bool:
        try:
            self.parse(message)
            return True
        except UnparsableError:
            return False

    def parse(self, message: str) -> Message:
        date, rest = self._parse_begin(message)
        person, rest = self._parse_person(rest)
        number, score = self._parse_game(rest)
        return Message(date, person, self.game, number, score)

    def _parse_begin(self, message: str):
        m = re.match(self.begin_regex, message)
        if not m:
            raise UnparsableError()

        return m.groups()

    def _parse_person(self, message: str):
        m = re.match(self.person_regex, message)
        if not m:
            raise UnparsableError()

        return m.groups()

    def _parse_game(self, message: str):
        m = re.match(self.game_regex, message)
        if not m:
            raise UnparsableError()

        return m.group("num"), m.group("score")


def is_new_message_line(line):
    """
    Determines if the message constitutes the first line of a message or not,
    in which case it would be a 'body' message.
    """
    return bool(re.match(BEGIN_RE, line))
