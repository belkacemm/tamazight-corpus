from dataclasses import dataclass


@dataclass(slots=True)
class RecorderConfig:
    """
    Configuration used by the recorder.
    """

    sample_rate: int = 16000
    channels: int = 1
    dtype: str = "int16"
