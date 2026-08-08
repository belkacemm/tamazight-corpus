from dataclasses import dataclass


@dataclass(slots=True)
class Transcript:
    """
    Transcript associated with one recording.
    """

    text: str
