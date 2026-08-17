import csv
from io import StringIO

from ..models.speaker import Speaker
from ..storage.supabase_storage import SupabaseStorage


class SupabaseSpeakerRepository:
    """
    Manage speakers stored in Supabase Storage.
    """

    def __init__(self, corpus_name: str):
        self.storage = SupabaseStorage(
            prefix=corpus_name
        )

        self.speakers_path = "metadata/speakers.csv"

    def create(self, speaker: Speaker):
        """
        Save a new speaker.
        """

        try:
            csv_text = self.storage.download_text(
                self.speakers_path
            )
        except Exception:
            csv_text = ""

        rows = (
            list(
                csv.DictReader(
                    csv_text.splitlines()
                )
            )
            if csv_text
            else []
        )

        if any(
            row["id"] == speaker.id
            for row in rows
        ):
            raise ValueError(
                f"Speaker {speaker.id} already exists."
            )

        headers = ["id", "name"]

        rows.append(
            {
                "id": speaker.id,
                "name": speaker.name or "",
            }
        )

        buffer = StringIO()

        writer = csv.DictWriter(
            buffer,
            fieldnames=headers,
        )

        writer.writeheader()
        writer.writerows(rows)

        self.storage.upload_text(
            buffer.getvalue(),
            self.speakers_path,
        )

    def get(
        self,
        speaker_id: str,
    ) -> Speaker | None:
        """
        Load one speaker.
        """

        try:
            csv_text = self.storage.download_text(
                self.speakers_path
            )
        except Exception:
            return None

        reader = csv.DictReader(
            csv_text.splitlines()
        )

        for row in reader:
            if row["id"] == speaker_id:
                return Speaker(
                    id=row["id"],
                    name=row["name"] or None,
                )

        return None

    def all(self) -> list[Speaker]:
        """
        Load all speakers.
        """

        try:
            csv_text = self.storage.download_text(
                self.speakers_path
            )
        except Exception:
            return []

        speakers = []

        reader = csv.DictReader(
            csv_text.splitlines()
        )

        for row in reader:
            speakers.append(
                Speaker(
                    id=row["id"],
                    name=row["name"] or None,
                )
            )

        return speakers