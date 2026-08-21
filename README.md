Tamazight Corpus Framework
A modular Python framework for creating, collecting, managing, validating, and storing speech corpora for Tamazight/Kabyle and other low-resource languages.

The framework provides both a command-line interface (CLI) and a Flask web application. It separates corpus-management logic from the storage layer, allowing the same corpus model to be used with local filesystem storage during development and persistent cloud storage during deployment.

The framework was initially developed for Tamazight/Kabyle speech corpus construction, but its design is intended to be reusable for other languages.

Features
Create corpus projects
Manage speakers
Record speech using a microphone
Upload existing audio files
Enter and edit transcripts
Associate recordings with speakers
Store recording metadata
Generate unique recording identifiers
Validate corpus structure and references
Play recordings through the web interface
Local filesystem storage
Supabase persistent storage
Flask web application
Command-line interface
Automated tests
Designed for low-resource speech-corpus collection
Architecture
The framework separates corpus-management logic, application interfaces, and physical storage.

                    Tamazight Corpus Framework
                              |
              +---------------+---------------+
              |                               |
         Python / CLI                    Flask Web App
              |                               |
              +---------------+---------------+
                              |
                       Corpus Project
                              |
                    +---------+---------+
                    |                   |
                 Speakers           Recordings
                    |                   |
               Repository          Repository
                                        |
                              +---------+---------+
                              |                   |
                       Local Storage       Supabase Storage
This separation allows the corpus-management components to operate independently of a particular web framework or storage provider.

Requirements
Python
Python 3.13 or newer is recommended.

Check your Python installation:

python --version
The v0.1.0 release was tested with Python 3.13.6.

uv
The project uses uv for Python environment and dependency management.

Install uv according to its official documentation.

Installation
Clone the repository:

git clone https://github.com/belkacemm/tamazight-corpus.git
cd tamazight-corpus
Install the project environment and dependencies:

uv sync
The environment is managed automatically by uv.

Reproducibility
The first evaluated software release is:

v0.1.0
The release was tested on Windows with:

Python 3.13.6
pytest 9.1.1
The test suite contains four tests.

Run:

uv run pytest
The expected result for the v0.1.0 release is:

4 passed
The tests cover core corpus, project, repository, and speaker functionality.

Command-Line Interface
The framework provides a command-line interface:

uv run python -m tamazight_corpus.cli --help
Available commands:

init
record
speaker
stats
validate
Create a corpus
For example:

uv run python -m tamazight_corpus.cli init test_corpus --name "Test Corpus" --language "Kabyle"
The framework creates the corpus structure and configuration.

A corpus contains:

test_corpus/
├── audio/
├── transcripts/
├── metadata/
└── corpus.yaml
Create a speaker
From inside the corpus directory:

uv run python -m tamazight_corpus.cli speaker create . SPK001 --name "Test Speaker"
List speakers:

uv run python -m tamazight_corpus.cli speaker list .
Example:

SPK001  Test Speaker
Record speech
Run:

uv run python -m tamazight_corpus.cli record .
The framework requests a speaker identifier, records speech, requests the transcript, and stores the recording.

Example:

Speaker ID: SPK001
Recording for 5.0 seconds...
Recording finished.
Transcript: Azul fellawen aken matalem
Saved recording 000001
View statistics
uv run python -m tamazight_corpus.cli stats .
Example:

Corpus: Publication Test Corpus
Recordings: 1
Speakers: 1
Duration: 5.0 seconds
Average: 5.0 seconds
Validate a corpus
uv run python -m tamazight_corpus.cli validate .
Example:

Corpus validation
=================
Recordings checked: 1
Speakers referenced: 1
Validation successful.
Errors found: 0
Corpus Data Model
Each recording is represented as a structured corpus record rather than as an isolated audio file.

A recording is associated with:

Recording ID
Speaker ID
Audio resource
Transcript
Sample rate
Number of channels
Duration
For example:

ID:          000001
Speaker:     SPK001
Audio:       000001.wav
Transcript:  000001.txt
Sample rate: 16000
Channels:    1
Duration:    5.00 seconds
The corresponding metadata can be represented in recordings.csv:

id,speaker,audio,transcript,sample_rate,channels,duration
000001,SPK001,000001.wav,000001.txt,16000,1,5.0
Corpus Structure
A corpus is organized approximately as follows:

corpus/
├── audio/
│   ├── 000001.wav
│   ├── 000002.wav
│   └── ...
│
├── transcripts/
│   ├── 000001.txt
│   ├── 000002.txt
│   └── ...
│
├── metadata/
│   ├── speakers.csv
│   └── recordings.csv
│
└── corpus.yaml
The corresponding conceptual model is:

Corpus
│
├── Speakers
│   ├── SPK001
│   ├── SPK002
│   └── ...
│
└── Recordings
    ├── Recording 000001
    │   ├── Audio
    │   ├── Transcript
    │   └── Metadata
    │
    ├── Recording 000002
    │   ├── Audio
    │   ├── Transcript
    │   └── Metadata
    │
    └── ...
This structure allows speaker-level information to remain associated with recordings and can later support the creation of machine-learning training, development, and test partitions.

Web Application
The project includes a Flask-based web application for browser-based corpus collection.

Start the application from the project root:

uv run python -m web.app
Alternatively, a Flask command can be used:

uv run flask --app web.app run
Then open:

http://127.0.0.1:5000/
The web application provides:

Corpus creation
Speaker management
Browser-based recording
Audio-file upload
Transcript entry
Recording metadata
Recording playback
Corpus statistics
Browser Recording
The web application uses the browser's MediaRecorder API for microphone recording.

Browser implementations may produce different audio representations, including formats such as WebM/Opus or WAV. Therefore, the application must handle the format actually received from the browser before incorporating the recording into the corpus.

The tested corpus records use:

Sample rate: 16000 Hz
Channels:    1
The browser recording workflow is:

Select speaker
      ↓
Start recording
      ↓
Speak
      ↓
Stop recording
      ↓
Provide transcript
      ↓
Submit
      ↓
Store audio and metadata
      ↓
View / play recording
Supabase Persistent Storage
For deployment, the framework can use Supabase Storage as persistent external storage.

The storage architecture is:

Browser
   |
   v
Flask Application
   |
   v
Tamazight Corpus Framework
   |
   v
Supabase Storage
A corpus can be stored approximately as:

<corpus-name>/
├── audio/
│   ├── 000001.wav
│   ├── 000002.wav
│   └── ...
│
├── transcripts/
│   ├── 000001.txt
│   ├── 000002.txt
│   └── ...
│
└── metadata/
    ├── speakers.csv
    └── recordings.csv
The external storage layer is important for deployment because the filesystem associated with a web-service instance should not be treated as the authoritative permanent location of corpus data.

Supabase Configuration
Create a Supabase project and configure a private Storage bucket.

The application uses environment variables such as:

SUPABASE_URL
SUPABASE_KEY
For local development, create a .env file:

SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
Never commit credentials to GitHub.

The repository already excludes environment files through .gitignore.

Local Storage and Cloud Storage
The framework separates corpus operations from physical storage.

Local storage
Local storage is useful for development and testing.

Conceptually:

project = Project.create(
    path=Path("datasets/kabyle"),
    config=config,
    storage="local",
)
Supabase storage
Supabase storage can be used for persistent deployment:

project = Project.create(
    path=Path("datasets/kabyle"),
    config=config,
    storage="supabase",
)
The exact storage configuration depends on the environment and configured credentials.

Render Deployment
The Flask application can be deployed to a service such as Render.

The deployment separates:

Application execution
        |
      Render
        |
        v
Tamazight Corpus Framework
        |
        v
Persistent corpus storage
        |
     Supabase
The application service can therefore be restarted or redeployed without requiring previously stored corpus resources to be recreated, provided that the external persistent storage remains available.

The v0.1.0 evaluation included application redeployment and verification that previously collected recordings remained available.

Python API
The framework can also be used directly from Python.

Example:

from pathlib import Path

from tamazight_corpus.models.config import CorpusConfig
from tamazight_corpus.models.project import Project

config = CorpusConfig(
    name="kabyle",
    language="Kabyle",
)

project = Project.create(
    path=Path("datasets/kabyle"),
    config=config,
    storage="local",
)
The framework can also be configured for an external storage backend where supported by the deployment configuration.

Speaker Management from Python
Example:

from tamazight_corpus.models.speaker import Speaker

speaker = Speaker(
    id="SPK001",
    name="Speaker One",
)

project.speakers.create(speaker)
Retrieve all speakers:

speakers = project.speakers.all()
Retrieve a speaker by identifier:

speaker = project.speakers.get("SPK001")
Recording Model
A recording conceptually contains:

Recording(
    id=...,
    audio=AudioFile(...),
    transcript=Transcript(...),
    speaker=...,
)
Audio information includes properties such as:

AudioFile(
    path=...,
    sample_rate=16000,
    channels=1,
    duration=...,
)
A transcript contains the textual transcription:

Transcript(
    text="Azul fellawen",
)
Project Structure
The principal repository structure is:

tamazight-corpus/
│
├── tamazight_corpus/
│   ├── audio/
│   ├── io/
│   ├── models/
│   ├── repositories/
│   ├── storage/
│   └── cli.py
│
├── web/
│   ├── app.py
│   ├── forms.py
│   ├── templates/
│   └── static/
│
├── tests/
│
├── datasets/
│
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
Local corpus data and recorded WAV files are intentionally excluded from the public Git repository.

Testing
Run the automated tests:

uv run pytest
The v0.1.0 release currently contains four tests covering core corpus functionality.

Run the code-quality checker:

uv run ruff check .
Example Corpus Collection
A corpus can grow through repeated speaker-recording pairs:

Speaker
   ↓
Sentence
   ↓
Audio recording
   ↓
Transcript
   ↓
Metadata
For example:

SPK001
   ├── 000001
   ├── 000002
   └── 000003

SPK002
   ├── 000004
   ├── 000005
   └── ...
A sufficiently large and well-documented corpus can subsequently be prepared for ASR and other speech-technology experiments.

Research Use
The framework was initially developed in the context of Tamazight/Kabyle speech-resource construction.

Its intended role is infrastructure for:

Corpus creation
Speech-data collection
Speaker management
Transcript management
Metadata organization
Data validation
Persistent storage
Preparation for downstream speech and machine-learning research
The framework itself is not an automatic speech-recognition model. It provides infrastructure for constructing the speech resources that can later be used to train or evaluate ASR systems.

Data and Privacy
Speech recordings can contain identifiable information and should be handled according to applicable consent, privacy, licensing, and research-ethics requirements.

The development repository does not include the speech recordings used during local testing.

Recorded audio files are excluded through .gitignore, including:

*.wav
The local publication test corpus is also excluded:

test_publication_corpus/
Researchers creating a corpus should establish appropriate consent, licensing, access-control, and data-retention procedures before collecting or distributing speech data.

Limitations
The current implementation has not been evaluated at large scale.

The v0.1.0 evaluation does not establish:

scalability to thousands or millions of recordings;
concurrent-user performance;
upload-throughput limits;
storage-cost characteristics;
linguistic representativeness;
transcription accuracy;
speaker or dialect balance;
superiority over existing speech-collection platforms.
These are subjects for future evaluation.

Roadmap
Potential future improvements include:

Automated audio-quality checks
Audio normalization
More extensive corpus statistics
Richer speaker metadata
Linguistic and dialect metadata
Consent and provenance metadata
Duplicate detection
Dataset export
Hugging Face dataset integration
Batch upload
ASR dataset preparation
Additional storage backends
Authentication and user management
Larger-scale performance evaluation
Contributing
Contributions are welcome.

Potential areas include:

New storage backends
Corpus validation
Audio processing
Dataset export
Web-interface improvements
ASR dataset preparation
Metadata improvements
Support for additional languages
License
This project is released under the MIT License.

See [LICENSE]LICENSE for the complete license text.

Release
The first evaluated release is:

v0.1.0
The release represents the software version used for the initial functional evaluation described in the accompanying research paper.

Citation
If this framework contributes to your research, please cite the accompanying research publication when available.

Until a formal publication is available, the GitHub repository and release version should be referenced explicitly:

Tamazight Corpus Framework, v0.1.0.
https://github.com/belkacemm/tamazight-corpus
Summary
The Tamazight Corpus Framework provides a modular foundation for collecting and managing structured speech data.

It separates:

Corpus management
       ↓
Application interface
       ↓
Physical storage
This allows researchers to develop locally, collect speech through a web interface, and use persistent external storage when deploying the application.

The framework was initially developed for Tamazight/Kabyle speech-corpus construction, with the broader goal of providing reusable infrastructure for researchers working with low-resource languages.