from dataclasses import dataclass


@dataclass(slots=True)
class Speaker:
    """
    Represents one speaker in the corpus.
    """

    id: str
    name: str | None = None