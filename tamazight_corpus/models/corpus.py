from .recording import Recording
from .transcript import Transcript
from .corpus_statistics import CorpusStatistics
from .speaker import Speaker

class Corpus:
    """
    Coordinates all corpus operations.
    """

    def __init__(self, repository, recorder):
        self.repository = repository
        self.recorder = recorder

    @property
    def recordings(self) -> list[Recording]:
        """
        Return all recordings in the corpus.
        """
        return self.repository.load_recordings()

    def __iter__(self):
        """
        Iterate over all recordings.
        """
        return iter(self.recordings)

    def record(self, speaker: Speaker) -> Recording:
        """
        Record one utterance and save it.
        """

        # Generate ID
        recording_id = self.repository.next_recording_id()

        # Determine audio path
        audio_path = self.repository.audio_path(recording_id)

        # Record audio
        audio = self.recorder.record(audio_path)

        # Ask researcher for transcript
        text = input("Transcript: ").strip()

        transcript = Transcript(text=text)

        # Create domain object
        recording = Recording(id=recording_id, audio=audio, transcript=transcript, speaker=speaker)

        # Persist recording
        self.repository.save_recording(recording)

        return recording

    def stats(self) -> CorpusStatistics:
        """
        Compute corpus statistics.
        """

        recordings = self.recordings

        total_duration = sum(
            recording.audio.duration
            for recording in recordings
        )

        speaker_ids = {
            recording.speaker.id
            for recording in recordings
        }

        return CorpusStatistics(
            recordings=len(recordings),
            speakers=len(speaker_ids),
            total_duration=total_duration
        )