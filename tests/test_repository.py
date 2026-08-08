from tamazight_corpus.repositories.file_repository import FileRepository


def test_first_recording_id(tmp_path):

    repo = FileRepository(tmp_path)

    recording_id = repo.next_recording_id()

    assert recording_id == "000001"
