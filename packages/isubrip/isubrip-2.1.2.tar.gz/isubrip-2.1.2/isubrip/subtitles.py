from typing import Iterator


class Timestamp:
    """An object representing a subtitles timestamp."""

    def __init__(self, hours: int, minutes: int, seconds: int, milliseconds: int):
        self.hours = hours

        if minutes < 60:
            self.minutes = minutes

        else:
            self.hours += minutes // 60
            self.minutes = minutes % 60

        if seconds < 60:
            self.seconds = seconds

        else:
            self.minutes += seconds // 60
            self.seconds = seconds % 60

        if milliseconds < 1000:
            self.milliseconds = milliseconds

        else:
            self.seconds += milliseconds // 1000
            self.milliseconds = milliseconds % 1000

        if self.hours > 99:
            raise ValueError("Timestamp hours cannot exceed 99.")

    def __str__(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.milliseconds:03}"


class Paragraph:
    """An object represnting a subtitles paragraph."""
    def __init__(self, start_time: Timestamp, end_time: Timestamp, text: str):
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def loads(self, line: str):
        """Loads a paragraph from a line of text."""
        lines = line.split("\n")

        self.start_time = Timestamp(*[int(x) for x in line[0].split(":")])
        self.end_time = Timestamp(*[int(x) for x in line[1].split(":")])
        self.text = line[2]


class Subtitles:
    """An object representing a subtitles file."""
    def __init__(self):
        self.paragraphs = []

    def add_paragraph(self, paragraph: Paragraph):
        self.paragraphs.append(paragraph)

    def __add__(self, paragraph: Paragraph):
        self.add_paragraph(paragraph)

    def loads(self, subtitles_str: str):
        pass

    def _parse_subtitles(self, line: str) -> Iterator[Paragraph]:
        """Parses a line of text into a paragraph."""
        pass
