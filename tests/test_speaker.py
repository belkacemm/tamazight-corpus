from tamazight_corpus.models.speaker import Speaker

def test_recording_keeps_speaker():
    speaker = Speaker(id="SP001")
    assert speaker.id == "SP001"