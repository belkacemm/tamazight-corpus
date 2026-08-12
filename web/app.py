from pathlib import Path

from flask import Flask, render_template, redirect, url_for
from .forms import CreateCorpusForm, CreateSpeakerForm

from tamazight_corpus.models.config import CorpusConfig
from tamazight_corpus.models.project import Project
from tamazight_corpus.models.speaker import Speaker


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

if __name__ == "__main__":
    app.run(debug=True)