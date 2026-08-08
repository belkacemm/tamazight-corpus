from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write

from ..models.audio_file import AudioFile
from .recorder_config import RecorderConfig


class Recorder:
    """
    Records audio from the microphone.
    """

    def __init__(self, config: RecorderConfig):
        self.config = config

    def record(self, output_path: Path, duration: float = 5.0) -> AudioFile:

        print(f"Recording for {duration} seconds...")

        audio = sd.rec(
            int(duration * self.config.sample_rate),
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            dtype=self.config.dtype,
        )

        sd.wait()

        write(output_path, self.config.sample_rate, audio)

        print("Recording finished.")

        return AudioFile(
            path=output_path,
            sample_rate=self.config.sample_rate,
            channels=self.config.channels,
            duration=duration,
        )
