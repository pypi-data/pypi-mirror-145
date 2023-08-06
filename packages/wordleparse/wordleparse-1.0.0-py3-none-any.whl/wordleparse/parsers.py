from wordleparse.parser import GameParser


num_re = r"[0-9]+"
basic_score_re = r"[1-6X]/6"

wordle_parser = GameParser(
    "Wordle", rf"Wordle (?P<num>{num_re}) (?P<score>{basic_score_re}\*?)\n"
)
woordle_parser = GameParser(
    "Woordle", rf"Woordle (?P<num>{num_re}) (?P<score>{basic_score_re})\n"
)
woordle6_parser = GameParser(
    "Woordle6", rf"Woordle6 (?P<num>{num_re}) (?P<score>{basic_score_re})\n"
)
worldle_parser = GameParser(
    "Worldle",
    r"#Worldle (?P<num>#[0-9]+) (?P<score>[1-6X]/6(?: \([0-9]{1,3}%\))?(?: 🙈)?)(?: 🙁)?\n",
)
squardle_win_parser = GameParser(
    "Squardle",
    r"I won Daily Squardle (?P<num>#[0-9]+) with (?P<score>[0-9]+) guess(?:es)? to spare!\n",
)
squardle_loss_parser = GameParser(
    "Squardle",
    r"I solved (?P<score>[0-9]{1,2}/21) squares in Daily Squardle (?P<num>#[0-9]+)\n",
)
crosswordle_parser = GameParser(
    "Crosswordle", r"Daily Crosswordle (?P<num>[0-9]+): (?P<score>[\w ]+) .*\n"
)
primel_parser = GameParser(
    "Primel", rf"Primel (?P<num>{num_re}) (?P<score>{basic_score_re})"
)
letterle_parser = GameParser("Letterle", r"Letterle(?P<num> )(?P<score>[0-9]{1,2}/26)")
not_wordle_parser = GameParser(
    "Not Wordle", rf"Not Wordle (?P<num>{num_re}) (?P<score>{basic_score_re})\n"
)
nerdle_parser = GameParser(
    "Nerdle",
    rf"(?:Nerdle|nerdlegame) (?P<num>{num_re}) (?P<score>{basic_score_re})\n",
)
vardle_parser = GameParser("Vardle", rf"Vardle (?P<num>{num_re}) (?P<score>[1-8X]/8)\n")
diffle_parser = GameParser(
    "Diffle",
    r"Diffle (?P<num>[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})\n(?P<score>[0-9]+ words / [0-9]+ letters)",
)
