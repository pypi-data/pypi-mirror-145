import unittest

from wordleparse.util import group


class TestMessageGrouper(unittest.TestCase):
    def test_simple_message(self):
        message = """23/01/2022, 13:16 - D: Wordle 218 3/6

⬛⬛⬛⬛⬛
🟨🟩🟩🟨⬛
🟩🟩🟩🟩🟩
""".split(
            "\n"
        )
        grouped = list(group(iter(message)))
        self.assertEqual(1, len(grouped))
        self.assertEqual([message], grouped)

    def test_multiple_messages(self):
        message = """23/01/2022, 14:53 - C: Primel 22 3/6

🟩⬜⬜⬜🟩
🟩⬜⬜🟩🟩
🟩🟩🟩🟩🟩
23/01/2022, 14:54 - C: Wordle 22 3/6

🟩🟩⬜🟩⬜
🟩🟩⬜🟩⬜
🟩🟩🟩🟩🟩
""".split(
            "\n"
        )
        grouped = list(group(iter(message)))
        self.assertEqual(2, len(grouped))
        self.assertEqual("23/01/2022, 14:54 - C: Wordle 22 3/6", grouped[1][0])


if __name__ == "__main__":
    unittest.main()
