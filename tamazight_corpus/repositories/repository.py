from abc import ABC, abstractmethod
from pathlib import Path

from ..models.recording import Recording


class Repository(ABC):
    """
    Abstract interface for corpus storage.
    """

    @abstractmethod
    def next_recording_id(self) -> str:
        """
        Return the next recording identifier.
        """

    @abstractmethod
    def audio_path(self, recording_id: str) -> Path:
        """
        Return the audio file path.
        """

    @abstractmethod
    def save_recording(self, recording: Recording):
        """
        Save a recording.
        """

    @abstractmethod
    def load_recordings(self) -> list[Recording]:
        """
        Load all recordings.
        """
