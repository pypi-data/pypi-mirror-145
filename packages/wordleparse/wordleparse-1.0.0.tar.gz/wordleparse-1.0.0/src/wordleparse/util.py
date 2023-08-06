from typing import Iterator, List

from wordleparse.parser import is_new_message_line


def group(lines: Iterator[str]) -> Iterator[List[str]]:
    """
    Groups one entire bundle of chat messages into separate messages.
    Whether or not messages belong to each other is determined by
    is_new_message_line, which determines if a specific line is the 'start'
    of a multiline message.
    """
    try:
        line = next(lines)
    except StopIteration:
        raise ValueError(
            "We couldn't find the first message. Is the chat export empty?"
        )

    while lines:
        message = [line]
        try:
            line = next(lines)
            while not is_new_message_line(line):
                message.append(line)
                line = next(lines)
        except StopIteration:
            yield message
            break
        yield message
