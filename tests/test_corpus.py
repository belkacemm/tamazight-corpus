from tamazight_corpus.models.audio_file import AudioFile
from tamazight_corpus.models.recording import Recording
from tamazight_corpus.models.transcript import Transcript
from tamazight_corpus.repositories.file_repository import FileRepository
from tamazight_corpus.models.speaker import Speaker


def test_save_and_load_recording(tmp_path):

    repo = FileRepository(tmp_path)

    audio = AudioFile(
        path=(tmp_path / "audio" / "000001.wav"),
        sample_rate=16000,
        channels=1,
        duration=5.0,
    )

    transcript = Transcript(text="Azul fellak")

    speaker = Speaker(id="SP001")
    recording = Recording(id="000001", audio=audio, transcript=transcript, speaker=speaker)

    # Save
    repo.save_recording(recording)

    # Load
    recordings = repo.load_recordings()

    assert len(recordings) == 1

    loaded = recordings[0]

    assert loaded.id == "000001"

    assert loaded.transcript.text == "Azul fellak"
