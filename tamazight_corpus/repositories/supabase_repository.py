import csv
from pathlib import Path

from ..models.recording import Recording
from .repository import Repository
from ..storage.supabase_storage import SupabaseStorage

from ..models.audio_file import AudioFile
from ..models.transcript import Transcript
from ..models.speaker import Speaker


class SupabaseRepository(Repository):
    """
    Repository implementation using Supabase Storage.
    """

    def __init__(
        self,
        corpus_name: str,
        temp_dir: Path | None = None,
    ):
        self.storage = SupabaseStorage(
            prefix=corpus_name
        )

        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        self.temp_dir = (PROJECT_ROOT / ".supabase_cache" / corpus_name)

        self.metadata_path = "metadata/recordings.csv"

    def next_recording_id(self) -> str:
        """
        Generate the next recording ID.
        """

        try:
            text = self.storage.download_text(
                self.metadata_path
            )
        except Exception:
            return "000001"

        lines = list(
            csv.DictReader(
                text.splitlines()
            )
        )

        if not lines:
            return "000001"

        last_id = int(lines[-1]["id"])

        return f"{last_id + 1:06d}"

    def audio_path(
        self,
        recording_id: str,
    ) -> Path:
        """
        Return a temporary local path for audio.
        """

        audio_dir = self.temp_dir / "audio"
        audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return audio_dir / f"{recording_id}.wav"

   

    def save_recording(
        self,
        recording: Recording,
    ):
        """
        Save recording audio, transcript,
        and metadata to Supabase.
        """

        # Audio
        self.storage.upload_file(
            recording.audio.path,
            f"audio/{recording.id}.wav",
            "audio/wav",
        )

        # Transcript
        self.storage.upload_text(
            recording.transcript.text,
            f"transcripts/{recording.id}.txt",
        )

        # Metadata
        try:
            csv_text = self.storage.download_text(
                self.metadata_path
            )
        except Exception:
            csv_text = ""

        rows = list(
            csv.DictReader(
                csv_text.splitlines()
            )
        ) if csv_text else []

        if not rows:
            headers = [
                "id",
                "speaker",
                "audio",
                "transcript",
                "sample_rate",
                "channels",
                "duration",
            ]
        else:
            headers = list(rows[0].keys())

        rows.append(
            {
                "id": recording.id,
                "speaker": recording.speaker.id,
                "audio": f"{recording.id}.wav",
                "transcript": f"{recording.id}.txt",
                "sample_rate": str(
                    recording.audio.sample_rate
                ),
                "channels": str(
                    recording.audio.channels
                ),
                "duration": str(
                    recording.audio.duration
                ),
            }
        )

        from io import StringIO

        buffer = StringIO()

        writer = csv.DictWriter(
            buffer,
            fieldnames=headers,
        )

        writer.writeheader()
        writer.writerows(rows)

        self.storage.upload_text(
            buffer.getvalue(),
            self.metadata_path,
        )

    def load_recordings(self) -> list[Recording]:
        """
        Load all recordings from Supabase.
        """

        try:
            csv_text = self.storage.download_text(
                self.metadata_path
            )
        except Exception:
            return []

        rows = list(
            csv.DictReader(
                csv_text.splitlines()
            )
        )

        recordings = []

        for row in rows:
            recording_id = row["id"]

            # Download audio to temporary local cache
            audio_path = self.audio_path(
                recording_id
            )

            self.storage.download_file(
                f"audio/{recording_id}.wav",
                audio_path,
            )

            # Download transcript
            transcript_text = (
                self.storage.download_text(
                    f"transcripts/{recording_id}.txt"
                )
            )

            audio = AudioFile(
                path=audio_path,
                sample_rate=int(
                    row["sample_rate"]
                ),
                channels=int(
                    row["channels"]
                ),
                duration=float(
                    row["duration"]
                ),
            )

            transcript = Transcript(
                text=transcript_text
            )

            speaker = Speaker(
                id=row["speaker"]
            )

            recording = Recording(
                id=recording_id,
                audio=audio,
                transcript=transcript,
                speaker=speaker,
            )

            recordings.append(recording)

        return recordings

    def update_transcript(
        self,
        recording_id: str,
        text: str,
    ):
        """
        Update the transcript of a recording.
        """

        self.storage.upload_text(
            text,
            f"transcripts/{recording_id}.txt",
        )