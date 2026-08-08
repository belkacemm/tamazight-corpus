from pathlib import Path

from tamazight_corpus.repositories.file_repository import FileRepository

repo = FileRepository(Path("kabyle_dataset"))

recordings = repo.load_recordings()

print("Number:", len(recordings))

for recording in recordings:
    print(recording.id)
    print(recording.speaker.id)
    print(recording.transcript.text)
