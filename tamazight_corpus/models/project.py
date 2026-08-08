from pathlib import Path

from ..audio.recorder import Recorder
from ..audio.recorder_config import RecorderConfig
from ..io.config_io import ConfigIO
from ..repositories.file_repository import FileRepository
from .config import CorpusConfig
from .corpus import Corpus
from ..repositories.speaker_repository import SpeakerRepository


class Project:
    """
    Represents one corpus project.
    """

    def __init__(self, path: Path, config: CorpusConfig, corpus: Corpus, speakers: SpeakerRepository):
        self.path = path
        self.config = config
        self.corpus = corpus
        self.speakers = speakers

    @classmethod
    def create(cls, path: Path, config: CorpusConfig):

        path.mkdir(parents=True, exist_ok=True)

        repository = FileRepository(path)

        speaker_repository = SpeakerRepository(path)

        recorder = Recorder(
            RecorderConfig(sample_rate=config.sample_rate, channels=config.channels)
        )

        corpus = Corpus(repository=repository, recorder=recorder)

        ConfigIO.save(path / "corpus.yaml", config)

        return cls(path=path, config=config, corpus=corpus, speakers=speaker_repository)

    @classmethod
    def open(cls, path: Path):

        config = ConfigIO.load(path / "corpus.yaml")

        repository = FileRepository(path)

        speaker_repository = SpeakerRepository(path)

        recorder = Recorder(
            RecorderConfig(sample_rate=config.sample_rate, channels=config.channels)
        )

        corpus = Corpus(repository=repository, recorder=recorder)

        return cls(path=path, config=config, corpus=corpus, speakers=speaker_repository)
