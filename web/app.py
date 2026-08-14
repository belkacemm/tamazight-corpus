from pathlib import Path

from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from .forms import CreateCorpusForm, CreateSpeakerForm

from tamazight_corpus.models.config import CorpusConfig
from tamazight_corpus.models.project import Project
from tamazight_corpus.models.speaker import Speaker

import soundfile as sf
from tamazight_corpus.models.audio_file import AudioFile
from tamazight_corpus.models.recording import Recording
from tamazight_corpus.models.transcript import Transcript

app = Flask(__name__)

app.config["SECRET_KEY"] = "development-key"

DATASETS_DIR = Path(__file__).resolve().parent.parent / "datasets"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create-corpus", methods=["GET", "POST"])
def create_corpus():
    form = CreateCorpusForm()

    if form.validate_on_submit():
        name = form.name.data
        language = form.language.data

        config = CorpusConfig(
            name=name,
            language=language,
        )

        corpus_path = DATASETS_DIR / name

        Project.create(
            path=corpus_path,
            config=config,
        )

        return redirect(url_for("corpus_dashboard", corpus_name=name))

    return render_template(
        "create_corpus.html",
        form=form,
    )

@app.route("/corpus/<corpus_name>")
def corpus_dashboard(corpus_name):
    corpus_path = DATASETS_DIR / corpus_name

    project = Project.open(corpus_path)

    stats = project.corpus.stats()

    return render_template(
        "corpus_dashboard.html",
        project=project,
        stats=stats,
    )

@app.route("/corpus/<corpus_name>/speakers")
def speakers(corpus_name):
    corpus_path = DATASETS_DIR / corpus_name

    project = Project.open(corpus_path)

    speakers = project.speakers.all()

    return render_template(
        "speakers.html",
        project=project,
        speakers=speakers,
    )

@app.route(
    "/corpus/<corpus_name>/speakers/create",
    methods=["GET", "POST"],
)
def create_speaker(corpus_name):
    corpus_path = DATASETS_DIR / corpus_name

    project = Project.open(corpus_path)

    form = CreateSpeakerForm()

    if form.validate_on_submit():
        speaker_id = form.speaker_id.data.strip()
        name = form.name.data.strip() or None

        existing = project.speakers.get(speaker_id)

        if existing is not None:
            form.speaker_id.errors.append(
                "This speaker ID already exists."
            )
        else:
            speaker = Speaker(
                id=speaker_id,
                name=name,
            )

            project.speakers.create(speaker)

            return redirect(
                url_for(
                    "speakers",
                    corpus_name=corpus_name,
                )
            )

    return render_template(
        "create_speaker.html",
        form=form,
        project=project,
    )


@app.route(
    "/corpus/<corpus_name>/upload-audio",
    methods=["POST"],
)
def upload_audio(corpus_name):
    corpus_path = DATASETS_DIR / corpus_name

    project = Project.open(corpus_path)

    # Get speaker
    speaker_id = request.form.get("speaker_id")

    if not speaker_id:
        return "No speaker selected.", 400

    # Get transcript
    transcript_text = request.form.get("transcript","").strip()
    
    if not transcript_text:
        return "Transcript is required.", 400

    speaker = project.speakers.get(speaker_id)

    if speaker is None:
        return "Speaker not found.", 400

    # Get audio
    audio_file = request.files.get("audio")

    if audio_file is None:
        return "No audio file received.", 400

    if not audio_file.filename:
        return "No filename provided.", 400

    # Generate recording ID
    recording_id = project.corpus.repository.next_recording_id()

    # Determine final WAV path
    audio_path = project.corpus.repository.audio_path(
        recording_id
    )

    # Save uploaded WAV
    audio_file.save(audio_path)

    # Inspect WAV
    data, sample_rate = sf.read(audio_path)

    if data.ndim == 1:
        channels = 1
    else:
        channels = data.shape[1]

    duration = len(data) / sample_rate

    # Create AudioFile
    audio = AudioFile(
        path=audio_path,
        sample_rate=sample_rate,
        channels=channels,
        duration=duration,
    )

    # Temporary transcript
    transcript = Transcript(text=transcript_text)

    # Create Recording
    recording = Recording(
        id=recording_id,
        audio=audio,
        transcript=transcript,
        speaker=speaker,
    )

    # Persist recording
    project.corpus.repository.save_recording(
        recording
    )

    return (
        f"Recording {recording_id} saved.<br>"
        f"Speaker: {speaker.id}<br>"
        f"Sample rate: {sample_rate}<br>"
        f"Channels: {channels}<br>"
        f"Duration: {duration:.2f} seconds"
    )    

@app.route("/corpus/<corpus_name>/recordings")
def upload_audio_page(corpus_name):
    corpus_path = DATASETS_DIR / corpus_name

    project = Project.open(corpus_path)

    speakers = project.speakers.all()
    recordings = project.corpus.recordings

    return render_template(
        "recordings.html",
        project=project,
        speakers=speakers,
        recordings=recordings,
    )

@app.route("/corpus/<corpus_name>/audio/<filename>")
def serve_audio(corpus_name, filename):
    corpus_path = DATASETS_DIR / corpus_name
    audio_dir = corpus_path / "audio"

    return send_from_directory(
        audio_dir,
        filename
    )

@app.route(
    "/corpus/<corpus_name>/recording/<recording_id>/transcript",
    methods=["POST"]
)
def update_transcript(corpus_name, recording_id):
    corpus_path = DATASETS_DIR / corpus_name

    project = Project.open(corpus_path)

    text = request.form.get("transcript", "").strip()

    if not text:
        return "Transcript is required.", 400

    project.corpus.repository.update_transcript(
        recording_id,
        text
    )

    return redirect(
        url_for(
            "upload_audio_page",
            corpus_name=corpus_name
        )
    )

if __name__ == "__main__":
    app.run(debug=True)