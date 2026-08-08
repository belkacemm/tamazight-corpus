from dataclasses import dataclass


@dataclass(slots=True)
class CorpusConfig:
    """
    Configuration of a corpus project.
    """

    name: str
    language: str

    sample_rate: int = 16000
    channels: int = 1

    audio_directory: str = "audio"
    transcript_directory: str = "transcripts"
    metadata_directory: str = "metadata"
