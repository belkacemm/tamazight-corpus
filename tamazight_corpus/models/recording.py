from dataclasses import dataclass

from .audio_file import AudioFile
from .transcript import Transcript
from .speaker import Speaker


@dataclass(slots=True)
class Recording:
    """
    One recording in the corpus.
    """

    id: str
    audio: AudioFile
    transcript: Transcript
    speaker: Speaker