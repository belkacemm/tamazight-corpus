from dataclasses import dataclass


@dataclass(slots=True)
class CorpusStatistics:
    """
    Statistics describing a corpus.
    """

    recordings: int
    speakers: int
    total_duration: float

    @property
    def hours(self) -> float:
        return self.total_duration / 3600

    @property
    def average_duration(self) -> float:
        if self.recordings == 0:
            return 0.0

        return self.total_duration / self.recordings