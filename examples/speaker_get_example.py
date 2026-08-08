from pathlib import Path

from tamazight_corpus.models.project import Project
from tamazight_corpus.models.speaker import Speaker


project = Project.open(
    Path("kabyle_dataset")
)

project.speakers.create(
    Speaker(
        id="SP001",
        name="Ahmed"
    )
)

speaker = project.speakers.get(
    "SP001"
)

print(speaker)