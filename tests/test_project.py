from tamazight_corpus.models.config import CorpusConfig
from tamazight_corpus.models.project import Project


def test_project_creation(tmp_path):

    config = CorpusConfig(name="Kabyle", language="kabyle")

    project_path = tmp_path / "kabyle_dataset"

    Project.create(project_path, config)

    assert project_path.exists()
    assert (project_path / "corpus.yaml").exists()

    assert (project_path / "audio").exists()

    assert (project_path / "transcripts").exists()

    assert (project_path / "metadata").exists()
