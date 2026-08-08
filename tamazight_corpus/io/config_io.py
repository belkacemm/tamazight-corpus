from pathlib import Path

import yaml

from ..models.config import CorpusConfig


class ConfigIO:
    """
    Handles saving and loading corpus configuration.
    """

    @staticmethod
    def save(path: Path, config: CorpusConfig):
        """
        Save configuration to YAML.
        """

        data = {
            "name": config.name,
            "language": config.language,
            "sample_rate": config.sample_rate,
            "channels": config.channels,
            "audio_directory": config.audio_directory,
            "transcript_directory": config.transcript_directory,
            "metadata_directory": config.metadata_directory,
        }

        with open(path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, allow_unicode=True, sort_keys=False)

    @staticmethod
    def load(path: Path) -> CorpusConfig:
        """
        Load configuration from YAML.
        """

        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return CorpusConfig(
            name=data["name"],
            language=data["language"],
            sample_rate=data.get("sample_rate", 16000),
            channels=data.get("channels", 1),
            audio_directory=data.get("audio_directory", "audio"),
            transcript_directory=data.get("transcript_directory", "transcripts"),
            metadata_directory=data.get("metadata_directory", "metadata"),
        )
