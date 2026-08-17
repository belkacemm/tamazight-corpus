# Tamazight Corpus Framework

A Python framework for creating, collecting, managing, and storing speech corpora.

The framework was initially developed for collecting **Tamazight/Kabyle speech data**, but it can be used to create speech corpora for other languages as well.

Each recording consists of:

- WAV audio
- Speaker
- Transcript
- Sample rate
- Number of channels
- Duration
- Recording ID

The framework provides both a **Python/CLI interface** and a **Flask web application**.

Persistent storage can be provided by **Supabase Storage**, allowing the application to run on platforms such as Render without losing corpus data after a restart or redeployment.

---

## Features

- Create corpus projects
- Manage speakers
- Record speech using a microphone
- Upload existing WAV files
- Enter and edit transcripts
- Validate audio information
- Automatically generate recording IDs
- Store recording metadata
- Store transcripts
- Play recordings from the web application
- Persistent cloud storage with Supabase
- Local filesystem storage for development
- Flask web interface
- Command-line interface
- Designed for low-resource language corpus collection

---

# 1. Architecture

The framework separates the corpus logic from the storage system.

```text
                    Tamazight Corpus Framework
                              |
             +----------------+----------------+
             |                                 |
        Python / CLI                       Flask Web App
             |                                 |
             +----------------+----------------+
                              |
                           Project
                              |
                     +--------+--------+
                     |                 |
                   Corpus           Speakers
                     |                 |
                 Repository       Repository
                     |
          +----------+----------+
          |                     |
    FileRepository      SupabaseRepository
          |                     |
      Local disk          Supabase Storage
This design allows the same corpus framework to work with different storage backends.
2. Requirements
Python
Python 3.13 or newer is recommended.
Check your Python version:
python --version
uv
The project uses uv for Python environment and dependency management.
Install uv from:
https://docs.astral.sh/uv/⁠�
3. Installation
Clone the repository:
git clone https://github.com/belkacemm/tamazight-corpus
cd tamazight-corpus
Create the environment and install dependencies:
uv sync
The project environment is managed automatically by uv.
4. Command Line Interface
The framework provides a CLI:
uv run tamazight-corpus --help
Available commands include:
init
record
speaker
stats
validate
For example:
uv run tamazight-corpus init
The CLI can be used to create and manage corpora without the web application.
5. Web Application
The project also includes a Flask web application.
The web application is useful for people who want to collect speech data without interacting directly with the Python API.
Start the application
From the project root:
uv run flask --app web.app run
Then open:
http://127.0.0.1:5000
6. Creating a Corpus
Open:
Create Corpus
Enter:
Corpus name
Language
For example:
Corpus name: kabyle-test
Language: Kabyle
Submit the form.
The corpus dashboard will then be displayed.
7. Adding Speakers
Open:
Speakers
Choose:
Create Speaker
Enter:
Speaker ID: SPK001
Name: Speaker One
Create the speaker.
You can create as many speakers as needed.
Example:
SPK001
SPK002
SPK003
...
Each recording is associated with one speaker.
8. Collecting Speech
Open:
Recordings
Select a speaker.
You can either:
Record using the microphone
Click:
Start Recording
Speak normally.
Then click:
Stop Recording
The browser recording is converted to:
WAV
16 kHz
Mono
16-bit PCM
before being stored.
Or upload an existing WAV
Select an existing WAV file.
9. Adding a Transcript
Enter the exact transcription of the recording.
For example:
Azul fellawen
The transcript is stored separately from the audio.
The recording therefore has:
000001.wav
000001.txt
10. Recording Information
For each recording, the framework stores:
Recording ID
Speaker
Audio file
Transcript
Sample rate
Channels
Duration
Example:
ID:          000001
Speaker:     SPK001
Sample rate: 16000
Channels:    1
Duration:    2.45 seconds
Transcript:  Azul fellawen
11. Playing Recordings
The recordings page contains an audio player.
Click:
Play
to listen to the recording.
When Supabase storage is enabled, the WAV is downloaded to a temporary local cache when necessary and then served to the browser.
The permanent copy remains in Supabase.
12. Persistent Storage with Supabase
For production or cloud deployment, Supabase Storage can be used.
The bucket should be configured as private.
The corpus is stored approximately as:
<corpus-name>/
│
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
This allows the Flask application to restart without losing the corpus.
13. Supabase Configuration
Create a Supabase project and a private Storage bucket.
The application uses two environment variables:
SUPABASE_URL
SUPABASE_KEY
Create a .env file locally:
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
Never commit .env to GitHub.
Add it to .gitignore:
.env
14. Render Deployment
The Flask application can be deployed to Render.
Configure the Render service with the required environment variables:
SUPABASE_URL
SUPABASE_KEY
The application uses Supabase for persistent corpus storage.
This is important because the local filesystem of a Render service should not be treated as permanent storage.
After deployment, users can:
Create a corpus
Create speakers
Upload or record WAV files
Add transcripts
Listen to recordings
Corpus data remains in Supabase after a Render restart or redeployment.
15. Local vs Supabase Storage
The framework supports two storage approaches.
Local storage
Useful for development:
Project.create(
    path=corpus_path,
    config=config,
    storage="local",
)
Data is stored on the local filesystem.
Supabase storage
Useful for deployment:
Project.create(
    path=corpus_path,
    config=config,
    storage="supabase",
)
Audio, transcripts, and metadata are stored in Supabase.
The Flask application currently uses Supabase storage.
16. Developer Usage
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
For Supabase:
project = Project.create(
    path=Path("datasets/kabyle"),
    config=config,
    storage="supabase",
)
17. Creating a Speaker
from tamazight_corpus.models.speaker import Speaker

speaker = Speaker(
    id="SPK001",
    name="Speaker One",
)

project.speakers.create(speaker)
Retrieve speakers:
speakers = project.speakers.all()
Retrieve one speaker:
speaker = project.speakers.get("SPK001")
18. Creating a Recording
A recording contains:
Recording(
    id=...,
    audio=AudioFile(...),
    transcript=Transcript(...),
    speaker=...,
)
The audio model contains:
AudioFile(
    path=...,
    sample_rate=16000,
    channels=1,
    duration=...,
)
The transcript model contains:
Transcript(
    text="Azul fellawen",
)
19. Corpus Structure
A corpus conceptually contains:
Corpus
│
├── Speakers
│
└── Recordings
      │
      ├── Audio
      ├── Transcript
      └── Metadata
Each recording has a unique identifier.
Example:
000001
000002
000003
20. Project Structure
The main project structure is:
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
├── README.md
└── .gitignore
21. Testing
Run the test suite with:
uv run pytest
Check code quality with:
uv run ruff check .
22. Why This Framework?
Low-resource languages often lack sufficiently large speech datasets.
The purpose of this framework is to make it easier to build those datasets.
For example, a Kabyle corpus can be collected as:
Speaker
   ↓
Sentence
   ↓
WAV recording
   ↓
Transcript
   ↓
Metadata
Thousands of such pairs can eventually be used to train or fine-tune speech recognition models.
23. Example Corpus
A speech corpus might eventually contain:
10 speakers
      ↓
1,000 recordings
      ↓
1,000 WAV files
      +
1,000 transcripts
The resulting dataset can then be prepared for machine-learning and ASR experiments.
24. Roadmap
Planned improvements include:
Better corpus statistics
Corpus validation
Recording quality checks
More metadata
Export to common dataset formats
Hugging Face dataset integration
Improved speaker management
Batch upload
Dataset preparation for ASR
Additional storage backends
Authentication and user management
25. Contributing
Contributions are welcome.
Possible areas include:
New storage backends
Corpus validation
Web interface improvements
Audio processing
Dataset export
ASR dataset preparation
Support for additional languages
26. License: MIT License
Summary
Tamazight Corpus Framework provides a simple way to collect and manage speech data while keeping the underlying corpus architecture independent from the web application and storage system.
It can be used locally for development or deployed with Flask and Supabase for persistent cloud-based corpus collection.
