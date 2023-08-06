from datetime import date
from dataclasses import dataclass


@dataclass
class Message:
    date: date
    person: str
    game: str
    number: str
    score: str
