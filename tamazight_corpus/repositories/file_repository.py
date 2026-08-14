import csv
from pathlib import Path

from ..models.audio_file import AudioFile
from ..models.recording import Recording
from ..models.transcript import Transcript
from .repository import Repository
from .. models.speaker import Speaker

class FileRepository(Repository):
    """
    Repository implementation using the filesystem.
    """

    def __init__(self, root: Path):
        self.root = root

        self.audio_dir = root / "audio"

        self.transcript_dir = root / "transcripts"

        self.metadata_dir = root / "metadata"

        self.recordings_csv = self.metadata_dir / "recordings.csv"

        self._create_directories()

    def _create_directories(self):
        """
        Create corpus directories.
        """

        self.audio_dir.mkdir(exist_ok=True)

        self.transcript_dir.mkdir(exist_ok=True)

        self.metadata_dir.mkdir(exist_ok=True)

    def next_recording_id(self) -> str:
        """
        Generate the next recording ID.
        """

        if not self.recordings_csv.exists():
            return "000001"

        with open(self.recordings_csv, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            return "000001"

        last_id = int(rows[-1]["id"])

        return f"{last_id + 1:06d}"

    def audio_path(self, recording_id: str) -> Path:
        """
        Return WAV path.
        """

        return self.audio_dir / f"{recording_id}.wav"

    def save_transcript(self, recording: Recording):
        """
        Save transcript text.
        """

        path = self.transcript_dir / f"{recording.id}.txt"

        path.write_text(recording.transcript.text, encoding="utf-8")

    def save_recording(self, recording: Recording):
        """
        Save recording metadata.
        """

        self.save_transcript(recording)

        new_file = not self.recordings_csv.exists()

        with open(self.recordings_csv, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if new_file:
                writer.writerow(
                    ["id","speaker" ,"audio", "transcript", "sample_rate", "channels", "duration"]
                )

            writer.writerow(
                [
                    recording.id,
                    recording.speaker.id,
                    recording.audio.path.name,
                    f"{recording.id}.txt",
                    recording.audio.sample_rate,
                    recording.audio.channels,
                    recording.audio.duration,
                ]
            )

    def update_transcript(self, recording_id: str, text: str):
        """
        Update the transcript of an existing recording.
        """
        path = self.transcript_dir / f"{recording_id}.txt"
        path.write_text(text, encoding="utf-8")

    def load_recordings(self) -> list[Recording]:
        """
        Load all recordings.
        """

        recordings = []

        if not self.recordings_csv.exists():
            return recordings

        with open(self.recordings_csv, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                audio = AudioFile(
                    path=(self.audio_dir / row["audio"]),
                    sample_rate=int(row["sample_rate"]),
                    channels=int(row["channels"]),
                    duration=float(row["duration"]),
                )

                transcript = Transcript(
                    text=(self.transcript_dir / row["transcript"]).read_text(
                        encoding="utf-8"
                    )
                )

                speaker = Speaker(id=row["speaker"])
                recording = Recording(id=row["id"], audio=audio, transcript=transcript, speaker=speaker)

                recordings.append(recording)

        return recordings
