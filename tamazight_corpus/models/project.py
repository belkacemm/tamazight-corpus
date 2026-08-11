from pathlib import Path

from ..io.config_io import ConfigIO
from ..repositories.file_repository import FileRepository
from ..repositories.speaker_repository import SpeakerRepository
from .config import CorpusConfig
from .corpus import Corpus


class Project:
    """
    Represents one corpus project.
    """

    def __init__(
        self,
        path: Path,
        config: CorpusConfig,
        corpus: Corpus,
        speakers: SpeakerRepository,
    ):
        self.path = path
        self.config = config
        self.corpus = corpus
        self.speakers = speakers

    @classmethod
    def create(cls, path: Path, config: CorpusConfig):
        path.mkdir(parents=True, exist_ok=True)

        repository = FileRepository(path)
        speaker_repository = SpeakerRepository(path)

        corpus = Corpus(repository=repository)

        ConfigIO.save(path / "corpus.yaml", config)

        return cls(
            path=path,
            config=config,
            corpus=corpus,
            speakers=speaker_repository,
        )

    @classmethod
    def open(cls, path: Path):
        config = ConfigIO.load(path / "corpus.yaml")

        repository = FileRepository(path)
        speaker_repository = SpeakerRepository(path)

        corpus = Corpus(repository=repository)

        return cls(
            path=path,
            config=config,
            corpus=corpus,
            speakers=speaker_repository,
        )

    def enable_recording(self):
        """
        Enable microphone recording for this project.

        The audio recorder is imported only when recording
        functionality is actually requested.
        """
        from ..audio.recorder import Recorder
        from ..audio.recorder_config import RecorderConfig

        recorder = Recorder(
            RecorderConfig(
                sample_rate=self.config.sample_rate,
                channels=self.config.channels,
            )
        )

        self.corpus.recorder = recorder