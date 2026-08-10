from pathlib import Path

from flask import Flask, render_template, redirect, url_for
from forms import CreateCorpusForm

from tamazight_corpus.models.config import CorpusConfig
from tamazight_corpus.models.project import Project


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

        return redirect(url_for("home"))

    return render_template(
        "create_corpus.html",
        form=form,
    )


if __name__ == "__main__":
    app.run(debug=True)