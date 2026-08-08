from pathlib import Path
import csv

from ..models.speaker import Speaker


class SpeakerRepository:
    """
    Manage speaker storage.
    """

    def __init__(self, root: Path):
        self.metadata_dir = root / "metadata"

        self.speakers_csv = (
            self.metadata_dir /
            "speakers.csv"
        )

        self.metadata_dir.mkdir(
            exist_ok=True
        )

    def create(
        self,
        speaker: Speaker
    ):
        """
        Save a new speaker.
        """

        new_file = (
            not self.speakers_csv.exists()
        )

        with open(
            self.speakers_csv,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if new_file:
                writer.writerow(
                    [
                        "id",
                        "name"
                    ]
                )

            writer.writerow(
                [
                    speaker.id,
                    speaker.name or ""
                ]
            )

    def get(
        self,
        speaker_id: str
    ) -> Speaker | None:
        """
        Load one speaker.
        """

        if not self.speakers_csv.exists():
            return None

        with open(
            self.speakers_csv,
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["id"] == speaker_id:

                    return Speaker(
                        id=row["id"],
                        name=row["name"] or None
                    )

        return None

    def all(self) -> list[Speaker]:
        """
        Load all speakers.
        """

        speakers = []

        if not self.speakers_csv.exists():
            return speakers

        with open(
            self.speakers_csv,
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                speakers.append(
                    Speaker(
                        id=row["id"],
                        name=row["name"] or None
                    )
                )

        return speakers