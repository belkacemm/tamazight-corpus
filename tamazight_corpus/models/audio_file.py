from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AudioFile:
    """
    Represents one audio file.
    """

    path: Path
    sample_rate: int
    channels: int
    duration: float
